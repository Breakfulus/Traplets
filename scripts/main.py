import pygame
from entities.tower import Tower
from entities.enemy import Enemy
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
towers = pygame.sprite.Group()
enemies = pygame.sprite.Group()

grid = Grid(c.GRID_HEIGHT, c.GRID_WIDTH, c.TILE_SIZE)

preview_tiles = set()

new_enemy = Enemy(0, 0, c.TILE_SIZE / 2, path, 100, 2, 100, 100, 0)
enemies.add(new_enemy)

place_system = PlacementSystem(grid)

place_system.mouse_position()
            
#Tower functions
def place_tower(pos):
    #Create new tower
    new_tower = Tower(pos[0], pos[1], c.TILE_SIZE / 2)
    #Check if tile already has tower in it
    can_place = True
    for  t in towers:
        if t.rect.colliderect(new_tower):
            can_place = False
            print("Can't place here!")
            break
    for e in enemies:
        if e.rect.colliderect(new_tower):
            can_place = False
    #only place if tile is empty
    if can_place == True:
        towers.add(new_tower)
        grid.set_tile(new_tower.y // c.TILE_SIZE, new_tower.x // c.TILE_SIZE, 1)
        print("Tower placed!")

def select_tower(mouse_pos):
    #Clicking on tower selects it, clicking off tower deselects it
    for t in towers:
        if t.rect.collidepoint(mouse_pos):
            print("Tower  Clicked!")
            t.selected = not t.selected
        else:
            t.selected = False

def remove_tower(tower):
    grid.set_tile(tower.y // c.TILE_SIZE, tower.x // c.TILE_SIZE, 0)
    towers.remove(tower)
    print("Tower removed!")

dragging = False

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
            #stop selecting, place/destroy towers in building selection, and clear selection area
            place_system.dragging = False
            for tile in place_system.preview_tiles:
                    #Build towers
                    if grid.is_empty(tile[1], tile[0]) and c.MODE == 0:
                        place_tower((tile[0] * c.TILE_SIZE, tile[1] * c.TILE_SIZE))
                    #Destroy towers if in select c.mode dragging
                    if not grid.is_empty(tile[1], tile[0]) and c.MODE == 1:
                        for t in towers:
                            if t.rect.collidepoint(tile[0] * c.TILE_SIZE + c.TILE_SIZE // 2, tile[1] * c.TILE_SIZE + c.TILE_SIZE // 2):
                                remove_tower(t)
            place_system.preview_tiles.clear()
    
    place_system.building_selection()
    #Draw section
    screen.fill('darkslateblue')

    #draw mouse indicator and get mouse position
    place_system.mouse_position()
    
    grid.get_mouse_tile_pos(mouse_pos)
    grid.draw_grid(screen)

    enemies.update()
    enemies.draw(screen)

    #Draw towers
    for t in towers:
        t.draw_range(screen)
    towers.update()
    towers.draw(screen)
    
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