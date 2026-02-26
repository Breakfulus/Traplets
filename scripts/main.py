import pygame
#from entities.tower import Tower
#from entities.enemy import Enemy
from systems.entity_manager import EntityManager
from utils.entity_definitions import ENEMY_DEFINITIONS
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
    
#hold tower position and data
# towers = pygame.sprite.Group()
# enemies = pygame.sprite.Group()

grid = Grid(c.GRID_HEIGHT, c.GRID_WIDTH, c.TILE_SIZE)

preview_tiles = set()

# new_enemy = Enemy(0, 0, c.TILE_SIZE / 2, path, 100, 2, 100, 100, 0)
# enemies.add(new_enemy)

place_system = PlacementSystem(grid)
place_system.selected_blueprint = None

# def select_tower(mouse_pos):
#     #Clicking on tower selects it, clicking off tower deselects it
#     for t in towers:
#         if t.rect.collidepoint(mouse_pos):
#             print("Tower  Clicked!")
#             t.selected = not t.selected
#         else:
#             t.selected = False

manager = EntityManager()
enemy_blueprint = ENEMY_DEFINITIONS['mushant']

mushant_enemy = manager.create_entity(enemy_blueprint, (0, 0), 'enemy')
print(mushant_enemy.movement_component['speed'])

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
                    select_tower(mouse_pos)

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
    
    place_system.building_selection()
    #Draw section
    screen.fill('darkslateblue')

    #draw mouse indicator and get mouse position
    place_system.mouse_position()
    
    grid.get_mouse_tile_pos(mouse_pos)
    grid.draw_grid(screen)

    # enemies.update()
    # enemies.draw(screen)

    # #Draw towers
    # for t in towers:
    #     t.draw_range(screen)
    # towers.update()
    # towers.draw(screen)
    
    #draw building selection

    place_system.draw(screen)
    
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
'''TODO: Make Grid
make enemies spawn on E
Make buildings
Make enemies pathfind to buildings
Combat system
'''