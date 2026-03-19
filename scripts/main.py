import pygame
import heapq
import random
from systems.entity_manager import EntityManager
from utils.entity_definitions import ENEMY_DEFINITIONS
from utils.entity_definitions import TOWER_DEFINITIONS
from entities.grid import Grid
from systems.placement_system import PlacementSystem
from systems.movement_system import MovementSystem
import utils.consts as c

pygame.init()

screen = pygame.display.set_mode((c.SCREEN_WIDTH + c.UI_PANEL, c.SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Traplet Tower Defense")

clock = pygame.time.Clock()

path = [
    (0 * c.TILE_SIZE + c.TILE_SIZE // 2, 0 * c.TILE_SIZE + c.TILE_SIZE // 2),
    (7 * c.TILE_SIZE + c.TILE_SIZE // 2, 7 * c.TILE_SIZE + c.TILE_SIZE // 2)
    ]

grid = Grid(c.GRID_HEIGHT, c.GRID_WIDTH, c.TILE_SIZE)

preview_tiles = set()

place_system = PlacementSystem(grid)

PLACETOWER = pygame.USEREVENT + 1
DESTROYTOWER = pygame.USEREVENT + 2

manager = EntityManager()
enemy_blueprint = ENEMY_DEFINITIONS['mushant']

mushant_enemy = manager.create_entity(enemy_blueprint, (0, 0), 'enemy')
enemy_movement = MovementSystem(mushant_enemy)
reset = None

class Node:

    def __init__(self, position, g=0, h=0, terrain_cost=0):
        self.position = position
        self.g = g + terrain_cost #cost to get to that tile from the start plus the penalty depending on terrain
        self.h = h #estimated cost to get from the current tile in the path to the goal tile
        self.f = self.g + self.h
        self.parent = None #breadcrumb

    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(grid, row, col):
    
    #Make sure the bounds check comes before detecting if the tile is filed.
    
    neighbors = []

    if row > 0 and grid.is_empty(row - 1, col):
        neighbors.append((row - 1, col))
    
    if col > 0 and grid.is_empty(row, col - 1):
        neighbors.append((row, col - 1))

    if row < c.GRID_HEIGHT - 1 and grid.is_empty(row + 1, col):
        neighbors.append((row + 1, col))
    
    if col < c.GRID_WIDTH - 1 and grid.is_empty(row, col + 1):
        neighbors.append((row, col + 1))

    return neighbors

def a_star_algorithm(grid, start_tile, goal_tile):
    open_list = [] #explorable tiles
    start_node = Node(start_tile, g=0, h=abs(start_tile[0] - goal_tile[0]) + abs(start_tile[1] - goal_tile[1]))
    heapq.heappush(open_list, start_node) #push the start node, dont need to specify f because node holds its own properties

    came_from = {}

    g_score = {start_tile: 0}
    closed_set = set()

    goal_x, goal_y = goal_tile
    if grid.get_tile(goal_x, goal_y) != None:
            best_tile = None
            best_distance = float('inf')

            neighbors = get_neighbors(grid, goal_x, goal_y)

            for row, col in neighbors:
                if 0 <= row < grid.grid_height and 0 <= col < grid.grid_width:
                    if grid.is_empty(row, col):

                        # convert tile → pixel center
                        tile_x = col * c.TILE_SIZE + c.TILE_SIZE // 2
                        tile_y = row * c.TILE_SIZE + c.TILE_SIZE // 2

                        dx = tile_x - mushant_enemy.position[0]
                        dy = tile_y - mushant_enemy.position[1]

                        distance = dx*dx + dy*dy  # squared distance (faster, no sqrt)

                        if distance < best_distance:
                            best_distance = distance
                            best_tile = (row, col)  # return as (x, y)
                            print(best_tile)

            goal_tile = best_tile

    while open_list and goal_tile != None: #while there are explorable tiles
        current = heapq.heappop(open_list) #takes what is currently explorable and processes it

        if current.position in closed_set: #if its already explored, skip the tile
            continue
        
        closed_set.add(current.position) #tell that weve already explored this tle for future ref

        if current.position == goal_tile:
            path = []
            node = current
            while node:
                path.append(node.position)
                node = node.parent
            path.reverse()
            return path

        neighbors = get_neighbors(grid, *current.position)

        for nx, ny in neighbors:
            neighbor = (nx, ny)
            terrain_cost = grid.get_tile(round(ny), round(nx))
            if terrain_cost == None: terrain_cost = 0
            tentative_g = current.g + 1 + terrain_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                h = abs(nx - goal_tile[0]) + abs(ny - goal_tile[1]) #the guess of how far from where we are to the goal
                neighbor_node = Node((nx, ny), g=tentative_g, h=h, terrain_cost=terrain_cost)
                neighbor_node.parent = current

                heapq.heappush(open_list, neighbor_node) #add the next node and its cost to the queue
    return None

running = True
while running:
    mouse_pos = place_system.mouse_position()

    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                pass
        
            if event.key == pygame.K_c:
                if c.MODE == 0: c.MODE = 1
                else: c.MODE = 0

        place_system.placement_system_events(event)
        
        if event.type == PLACETOWER:
            manager.create_entity(event.blueprint, event.pos, event.team, event.eid)
            
            build_x, build_y = event.pos
            goal_tile = [build_y // c.TILE_SIZE, build_x // c.TILE_SIZE]
            start_tile = (int(mushant_enemy.position[1] // c.TILE_SIZE), int(mushant_enemy.position[0] // c.TILE_SIZE))

            path_tiles = a_star_algorithm(grid, start_tile, goal_tile)
            if path_tiles:
                pixel_path = [(y * c.TILE_SIZE, x * c.TILE_SIZE) for (x, y) in path_tiles]
                movement = getattr(mushant_enemy, "movement_component", None)
                movement['path'] = pixel_path
                movement['target_index'] = 0

        if event.type == DESTROYTOWER:
            manager.kill_entity(event.eid)
    
    place_system.building_selection()
    #Draw section
    screen.fill('darkslateblue')

    #draw mouse indicator and get mouse position
    place_system.mouse_position()
    
    grid.get_mouse_tile_pos(mouse_pos)
    grid.draw_grid(screen)

    enemy_movement.move_towards_target()
    
    manager.render_entities(screen)
    place_system.draw(screen)
    
    manager.entity_clean_up()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()