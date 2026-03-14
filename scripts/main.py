import pygame
from systems.entity_manager import EntityManager
from utils.entity_definitions import ENEMY_DEFINITIONS
from utils.entity_definitions import TOWER_DEFINITIONS
from entities.grid import Grid
from systems.placement_system import PlacementSystem
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
                for t in towers:
                    if t.selected:
                        remove_tower(t)
        
            if event.key == pygame.K_c:
                if c.MODE == 0: c.MODE = 1
                else: c.MODE = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.__getattribute__('button') == 1:
                if c.MODE == 0: 
                    place_system.preview_tiles.clear()
                    place_system.dragging = True
                else: 
                    place_system.preview_tiles.clear()
                    place_system.dragging = False

            elif event.__getattribute__('button') == 3:
                #Cancel selection with right click while selecting
                if c.MODE == 0:
                    place_system.preview_tiles.clear()
                    place_system.dragging = False
                #If not building and dragging right click quick destroy
                elif c.MODE == 1:
                    place_system.preview_tiles.clear()
                    place_system.dragging = True     
        
        if event.type == pygame.MOUSEBUTTONUP:
            if c.MODE == 0:
                place_system.finalize_placement()
            else:
                place_system.finalize_destruction()

            place_system.preview_tiles.clear()
        
        if event.type == PLACETOWER:
            manager.create_entity(event.blueprint, event.pos, event.team, event.eid)

        if event.type == DESTROYTOWER:
            manager.kill_entity(event.eid)
    
    place_system.building_selection()
    #Draw section
    screen.fill('darkslateblue')

    #draw mouse indicator and get mouse position
    place_system.mouse_position()
    
    grid.get_mouse_tile_pos(mouse_pos)
    grid.draw_grid(screen)
    
    manager.render_entities(screen)
    place_system.draw(screen)
    
    manager.entity_clean_up()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()