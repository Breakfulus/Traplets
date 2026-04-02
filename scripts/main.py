import pygame
from systems.entity_manager import EntityManager
from entities.grid import Grid
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

manager = EntityManager()

mushant_1 = manager.create_entity(ENEMY_DEFINITIONS['mushant'], (0 * c.TILE_SIZE, 0 * c.TILE_SIZE), 'enemy')
mushant_2 = manager.create_entity(ENEMY_DEFINITIONS['mushant'], (3 * c.TILE_SIZE, 0 * c.TILE_SIZE), 'enemy')
enemy_movement = MovementSystem()

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

            for entity in manager.enemies.values():
                movement = getattr(entity, "movement_component", None)
                movement['goal'] = event.pos
                movement['needs_path'] = True
            pathfinding_system.update(manager.enemies, grid)

        if event.type == DESTROYTOWER:
            manager.kill_entity(event.eid)
        
        if event.type == SELECTTOWER:
            print(f"Entity {event.eid} selected!")
            manager.select_entity(event.eid)
    
    place_system.building_selection()
    #Draw section
    screen.fill('darkslateblue')

    #draw mouse indicator and get mouse position
    place_system.mouse_position()
    
    grid.get_mouse_tile_pos(mouse_pos)
    grid.draw_grid(screen)

    enemy_movement.update(manager.enemies)
    
    manager.render_entities(screen)
    place_system.draw(screen)
    
    manager.entity_clean_up()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()