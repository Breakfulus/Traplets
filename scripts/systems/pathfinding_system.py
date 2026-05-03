import pygame
import heapq
import utils.consts as c

class Node:

    def __init__(self, position, g=0, h=0, terrain_cost=0):
        self.position = position
        self.g = g + terrain_cost #cost to get to that tile from the start plus the penalty depending on terrain
        self.h = h #estimated cost to get from the current tile in the path to the goal tile
        self.f = self.g + self.h
        self.parent = None #breadcrumb

    def __lt__(self, other):
        return self.f < other.f

class PathfindingSystem:
    def __init__(self):
        pass

    def get_neighbors(self, grid, row, col, goal_tile):
        
        #Make sure the bounds check comes before detecting if the tile is filed.
        
        neighbors = []

        if row > 0 and grid.is_not_blocked(row - 1, col) or (row - 1, col) == goal_tile:
            neighbors.append((row - 1, col))
        
        if col > 0 and grid.is_not_blocked(row, col - 1) or (row, col - 1) == goal_tile:
            neighbors.append((row, col - 1))

        if row < c.GRID_HEIGHT - 1 and grid.is_not_blocked(row + 1, col) or (row + 1, col) == goal_tile:
            neighbors.append((row + 1, col))
        
        if col < c.GRID_WIDTH - 1 and grid.is_not_blocked(row, col + 1) or (row, col + 1) == goal_tile:
            neighbors.append((row, col + 1))

        return neighbors

    def a_star_algorithm(self, grid, start_tile, goal_tile, entity):
        movement = entity.movement_component
        open_list = [] #explorable tiles
        start_node = Node(start_tile, g=0, h=abs(start_tile[0] - goal_tile[0]) + abs(start_tile[1] - goal_tile[1]))
        heapq.heappush(open_list, start_node) #push the start node, dont need to specify f because node holds its own properties

        came_from = {}

        g_score = {start_tile: 0}
        closed_set = set()

        goal_x, goal_y = goal_tile

        print("FINAL GOAL TILE:", goal_tile)
        
        # if grid.get_tile(goal_x, goal_y, c.STRUCTURES):

        #     if movement.get('final_tile') is None:
        #         best_tile = None
        #         best_distance = float('inf')

        #         neighbors = self.get_neighbors(grid, goal_x, goal_y)

        #         for row, col in neighbors:
        #             if not grid.is_not_blocked(row, col):
        #                 continue

        #             tile_x = col * c.TILE_SIZE + c.TILE_SIZE // 2
        #             tile_y = row * c.TILE_SIZE + c.TILE_SIZE // 2

        #             dx = tile_x - entity.position[0]
        #             dy = tile_y - entity.position[1]

        #             distance = dx*dx + dy*dy

        #             if distance < best_distance:
        #                 best_distance = distance
        #                 best_tile = (row, col)

        #         if best_tile is not None:
        #             movement['final_tile'] = best_tile
        #     goal_tile = movement.get('final_tile')

        #     goal_tile = movement.get('final_tile')

        #     if goal_tile == None:
        #         return None
        movement['final_tile'] = goal_tile

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

            neighbors = self.get_neighbors(grid, *current.position, goal_tile)

            for nx, ny in neighbors:
                neighbor = (nx, ny)
                terrain_cost = grid.get_tile(round(ny), round(nx), c.STRUCTURES)
                if terrain_cost == []: terrain_cost = 0
                else: terrain_cost = terrain_cost[0]
                tentative_g = current.g + 1 + terrain_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g

                    h = abs(nx - goal_tile[0]) + abs(ny - goal_tile[1]) #the guess of how far from where we are to the goal
                    neighbor_node = Node((nx, ny), g=tentative_g, h=h, terrain_cost=terrain_cost)
                    neighbor_node.parent = current

                    heapq.heappush(open_list, neighbor_node) #add the next node and its cost to the queue
        return None

    def generate_path(self, entity, movement, grid):
        
        goal_tile = None

        try:
            goal_tile = movement['goal'].position
            entity.movement_component["final_tile"]
        except: 
            return None

        if goal_tile is None:
            entity.movement_component["final_tile"]
            return None

        goal_tile = (goal_tile[1] // c.TILE_SIZE, goal_tile[0] // c.TILE_SIZE)
        entity.movement_component["final_tile"]
        # print(goal_tile)
        start_tile = (int(entity.position[1] // c.TILE_SIZE), int(entity.position[0] // c.TILE_SIZE))

        path_tiles = self.a_star_algorithm(grid, start_tile, goal_tile, entity)
        
        if path_tiles:
            pixel_path = [(col * c.TILE_SIZE + c.TILE_SIZE // 2, row * c.TILE_SIZE + c.TILE_SIZE // 2) for (row, col) in path_tiles]
            movement['path'] = pixel_path
            movement['target_index'] = 0
        else:
            entity.movement_component["path"] = []
            entity.movement_component["target"] = 0
            movement['final_tile'] = None
            
        movement['needs_path'] = False
        print("path generated!")
    
    def get_possible_goals(self, enemy, entities, preferences): #grab a goal from selected goals list

        goals = []

        for entity in entities.values():
            structure = getattr(entity, "structure_component", None)

            if not structure:
                continue
            
            if entity.need.get('type') not in preferences:
                print("Preference LOG:", enemy.need.get('type'), preferences)
                continue

            goals.append(entity)

        return goals
    
    def distance(self, a, b):
        ax, ay = a
        bx, by = b
        return abs(ax - bx) + abs(ay - by)
    
    def get_new_goal(self, goals, entity):

        if not goals:
            return
        
        goal = min(goals, key=lambda g: self.distance(entity.position, g.position))
        print("Entity Goal:", goal)
        return goal
    
    def check_if_path_dirty(self, entity, grid): #Check to see if the path is blocked while moving to the goal
        if not entity.movement_component["path"]:
            entity.movement_component["needs_path"] = True
            return
        
        for tile in entity.movement_component["path"]:
            row = tile[1] // c.TILE_SIZE
            col = tile[0] // c.TILE_SIZE

            if (row, col) == entity.movement_component["final_tile"]:
                continue

            if not grid.is_not_blocked(row, col):
                print("Path blocked, reclalculating...")
                entity.movement_component["path_dirty"] = True
                return

    def update(self, entities, structures, grid):
            for entity in entities.values():
                movement = getattr(entity, "movement_component", None)

                if not movement:
                    continue

                self.check_if_path_dirty(entity, grid)

                goals = self.get_possible_goals(entity, structures, movement["prefered_targets"])
                goal = self.get_new_goal(goals, entity)

                if movement["path_dirty"]:
                    movement["goal"] = goal 
                    movement["final_tile"] = None
                    movement["needs_path"] = True
                    movement["path_dirty"] = False

                if movement.get("goal") is None:
                    movement["goal"] = goal 
                    movement["final_tile"] = None

                if movement["needs_path"]:
                    self.generate_path(entity, movement, grid)
