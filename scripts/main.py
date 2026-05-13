import pygame
from grid import Grid
from systems.entity_manager import EntityManager
from systems.placement_system import PlacementSystem
from systems.movement_system import MovementSystem
from systems.pathfinding_system import PathfindingSystem
from systems.combat_system import CombatSystem
import utils.consts as c
from utils.entity_definitions import *


pygame.init()

PLACETOWER = pygame.USEREVENT + 1
DESTROYTOWER = pygame.USEREVENT + 2
SELECTTOWER = pygame.USEREVENT + 3

screen = pygame.display.set_mode((c.SCREEN_WIDTH + c.UI_PANEL, c.SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE | pygame.FULLSCREEN)
pygame.display.set_caption("Traplet Tower Defense")

clock = pygame.time.Clock()

grid = Grid(c.GRID_HEIGHT, c.GRID_WIDTH, c.TILE_SIZE)

place_system = PlacementSystem(grid)
preview_tiles = set()

manager = EntityManager(grid)

combat_system = CombatSystem(manager)

enemy_movement = MovementSystem()
pathfinding_system = PathfindingSystem()
pathfinding_system.update(manager.enemies, manager.entities, grid)

mushant_1 = manager.create_entity(ENEMY_DEFINITIONS['template'], (0 * c.TILE_SIZE + c.TILE_SIZE // 2, 0 * c.TILE_SIZE + c.TILE_SIZE // 2), [(0, 0)], 'enemy')
mushant_1 = manager.create_entity(ENEMY_DEFINITIONS['template'], (0 * c.TILE_SIZE + c.TILE_SIZE // 2, 1 * c.TILE_SIZE + c.TILE_SIZE // 2), [(1, 0)], 'enemy')
mushant_1 = manager.create_entity(ENEMY_DEFINITIONS['template'], (0 * c.TILE_SIZE + c.TILE_SIZE // 2, 2 * c.TILE_SIZE + c.TILE_SIZE // 2), [(2, 0)], 'enemy')

base = manager.create_entity(TOWER_DEFINITIONS['base'], (4 * c.TILE_SIZE + c.TILE_SIZE // 2, 4 * c.TILE_SIZE + c.TILE_SIZE // 2), [(4, 4)], 'player')
c.GAME_STATE = 0

running = True
while running:

    if c.GAME_STATE == 0: #Actively playing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            place_system.placement_system_events(event)
        
            if event.type == PLACETOWER:
                manager.create_entity(event.blueprint, event.pos, event.tiles, event.team)

            if event.type == DESTROYTOWER:
                if manager.entities[event.eid].structure_component["destructible"]:
                    manager.entities[event.eid].alive = False
                else:
                    continue
            
            if event.type == SELECTTOWER:
                print(f"Entity {event.eid} selected!")
                manager.select_entity(event.eid)

        mouse_pos = place_system.mouse_position()
        
        #Add selected tiles during building to selection
        place_system.building_selection()
        
        #Make enemies move
        pathfinding_system.update(manager.enemies, manager.entities, grid)
        enemy_movement.update(manager.entities, grid)
        combat_system.update(grid, list(manager.entities.values()))
        
        grid.update()

        #---Draw section---
        screen.fill('darkslateblue')

        grid.draw_grid(screen)

        manager.render_entities(screen)

        place_system.draw(screen)

        #Delete all entities who have a false alive flag at the end of a frame
        manager.entity_clean_up()
    else: #Lose scenario screen

        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

                if event.key == pygame.K_SPACE:
                    for entity in manager.entities.values():
                        entity.alive = False

                    manager.entity_clean_up() #clear up the entities before the loop resets
                    
                    mushant_1 = manager.create_entity(ENEMY_DEFINITIONS['template'], (0 * c.TILE_SIZE + c.TILE_SIZE // 2, 0 * c.TILE_SIZE + c.TILE_SIZE // 2), [(0, 0)], 'enemy')
                    mushant_1 = manager.create_entity(ENEMY_DEFINITIONS['template'], (0 * c.TILE_SIZE + c.TILE_SIZE // 2, 1 * c.TILE_SIZE + c.TILE_SIZE // 2), [(1, 0)], 'enemy')
                    mushant_1 = manager.create_entity(ENEMY_DEFINITIONS['template'], (0 * c.TILE_SIZE + c.TILE_SIZE // 2, 2 * c.TILE_SIZE + c.TILE_SIZE // 2), [(2, 0)], 'enemy')

                    base = manager.create_entity(TOWER_DEFINITIONS['base'], (4 * c.TILE_SIZE + c.TILE_SIZE // 2, 4 * c.TILE_SIZE + c.TILE_SIZE // 2), [(4, 4)], 'player')
                    c.GAME_STATE = 0

        screen.fill('darkslateblue')

    pygame.display.flip()
    clock.tick(60)

pygame.quit()