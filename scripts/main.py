import pygame
from tower import Tower
from enemy import Enemy
from systems.placement_system import Grid
from utils import consts as c

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

def mouse_position(): #get position of the tile mouse is hopvering over and indicate where the tower is placed
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col = mouse_x // c.TILE_SIZE
    row = mouse_y // c.TILE_SIZE
    cell_x = col * c.TILE_SIZE
    cell_y = row * c.TILE_SIZE
    center_x = cell_x + c.TILE_SIZE // 2
    center_y = cell_y + c.TILE_SIZE // 2
    return center_x, center_y

def building_selection():
    #drag selecting
    if dragging:
        tile_x, tile_y = mouse_pos[0] // c.TILE_SIZE, mouse_pos[1] // c.TILE_SIZE
        if 0 <= tile_x < c.GRID_WIDTH and 0 <= tile_y < c.GRID_HEIGHT:
            preview_tiles.add((tile_x, tile_y))
            print(preview_tiles)

def draw_selection():
    selected_rect = pygame.Rect(tile[0] * c.TILE_SIZE, tile[1] * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE)
    selected_tile  = pygame.Surface((c.TILE_SIZE, c.TILE_SIZE))
    if grid.is_empty(tile[1],tile[0]):
        color = (0, 200, 0)
    else:
        color = (200, 0, 0)
    selected_tile.fill(color)
    selected_tile.set_alpha(125)
    screen.blit(selected_tile, selected_rect)
    pygame.draw.rect(screen, (20, 20, 20, 50), selected_rect, 1)
            
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
    mouse_pos = mouse_position()

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
                    preview_tiles.clear()
                    dragging = True
                else: 
                    preview_tiles.clear()
                    dragging = False
                    select_tower(mouse_pos)

            elif event.__getattribute__('button') == 3:
                #Cancel selection with right click while selecting
                if c.MODE == 0:
                    preview_tiles.clear()
                    dragging = False
                #If not building and dragging right click quick destroy
                elif c.MODE == 1:
                    preview_tiles.clear()
                    dragging = True     
        
        if event.type == pygame.MOUSEBUTTONUP:
            #stop selecting, place/destroy towers in building selection, and clear selection area
            dragging = False
            for tile in preview_tiles:
                    #Build towers
                    if grid.is_empty(tile[1], tile[0]) and c.MODE == 0:
                        place_tower((tile[0] * c.TILE_SIZE, tile[1] * c.TILE_SIZE))
                    #Destroy towers if in select c.mode dragging
                    if not grid.is_empty(tile[1], tile[0]) and c.MODE == 1:
                        for t in towers:
                            if t.rect.collidepoint(tile[0] * c.TILE_SIZE + c.TILE_SIZE // 2, tile[1] * c.TILE_SIZE + c.TILE_SIZE // 2):
                                remove_tower(t)
            preview_tiles.clear()
    
    building_selection()
    #Draw section
    screen.fill('darkslateblue')

    #draw mouse indicator and get mouse position
    mouse_position()
    
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
    for tile in preview_tiles:
        draw_selection()
    
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
'''TODO: Make Grid
make enemies spawn on E
Make buildings
Make enemies pathfind to buildings
Combat system
'''