import pygame
from systems.entity_manager import EntityManager
from grid import Grid
from systems.placement_system import PlacementSystem
from systems.movement_system import MovementSystem
from systems.pathfinding_system import PathfindingSystem
from utils.entity_definitions import ENEMY_DEFINITIONS, TOWER_DEFINITIONS
import utils.consts as c

pygame.init()

screen = pygame.display.set_mode((c.SCREEN_WIDTH + c.UI_PANEL, c.SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Traplet Tower Defense")

clock = pygame.time.Clock()

path = []

grid = Grid(c.GRID_HEIGHT, c.GRID_WIDTH, c.TILE_SIZE)

preview_tiles = set()

place_system = PlacementSystem(grid)
pathfinding_system = PathfindingSystem()

PLACETOWER = pygame.USEREVENT + 1
DESTROYTOWER = pygame.USEREVENT + 2
SELECTTOWER = pygame.USEREVENT + 3

manager = EntityManager(grid)

mushant_1 = manager.create_entity(ENEMY_DEFINITIONS['mushant'], (0 * c.TILE_SIZE, 0 * c.TILE_SIZE), [(0, 0)], 'enemy')
base = manager.create_entity(TOWER_DEFINITIONS['base'], (4 * c.TILE_SIZE, 4 * c.TILE_SIZE), [(4, 4)], 'player')
enemy_movement = MovementSystem()

pathfinding_system.update(manager.enemies, manager.entities, grid)

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
        
            if event.key == pygame.K_c:
                if c.MODE == 0: c.MODE = 1
                else: c.MODE = 0

        place_system.placement_system_events(event)
        
        if event.type == PLACETOWER:
            manager.create_entity(event.blueprint, event.pos, event.tiles, event.team)
            

        if event.type == DESTROYTOWER:
            manager.kill_entity(event.eid, c.STRUCTURES)
        
        if event.type == SELECTTOWER:
            print(f"Entity {event.eid} selected!")
            manager.select_entity(event.eid)
    
    #Add selected tiles during building to selection
    place_system.building_selection()
    
    #Make enemies move
    pathfinding_system.update(manager.enemies, manager.entities, grid)
    enemy_movement.update(manager.enemies, grid, screen)
    
    grid.update()

    #---Draw section
    screen.fill('darkslateblue')

    grid.draw_grid(screen)

    manager.render_entities(screen)

    place_system.draw(screen)

    #Delete all entities who have a false alive flag at the end of a frame
    manager.entity_clean_up()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()