import pygame
from tower import Tower
from enemy import Enemy

pygame.init()

GRID_WIDTH = 11
GRID_HEIGHT = 11
TILE_SIZE = 64
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
GRAY = (15, 15, 15)
MODE = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Traplet Tower Defense")

clock = pygame.time.Clock()

path = [
    (0 * TILE_SIZE + TILE_SIZE // 2, 0 * TILE_SIZE + TILE_SIZE // 2),
    (7 * TILE_SIZE + TILE_SIZE // 2, 7 * TILE_SIZE + TILE_SIZE // 2)
    ]
#hold tower position and data
tower_list = []
enemy_list = []

grid = []
#make grid scale to consts
for row in range(GRID_HEIGHT):
    layer = []
    for col in range(GRID_WIDTH):
        layer.append(0)
    grid.append(layer)

preview_tiles = set()

new_enemy = Enemy(0, 0, TILE_SIZE / 2, path, 100, 2, 100, 100, 0)
enemy_list.append(new_enemy)

def mouse_position(): #get position of the tile mouse is hopvering over and indicate where the tower is placed
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col = mouse_x // TILE_SIZE
    row = mouse_y // TILE_SIZE
    cell_x = col * TILE_SIZE
    cell_y = row * TILE_SIZE
    center_x = cell_x + TILE_SIZE // 2
    center_y = cell_y + TILE_SIZE // 2
    return center_x, center_y

def building_selection():
    #drag selecting
    if dragging:
        tile_x, tile_y = mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE
        if 0 <= tile_x < GRID_WIDTH and 0 <= tile_y < GRID_HEIGHT:
            preview_tiles.add((tile_x, tile_y))
            print(preview_tiles)

def draw_selection():
    selected_rect = pygame.Rect(tile[0] * TILE_SIZE, tile[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    selected_tile  = pygame.Surface((TILE_SIZE, TILE_SIZE))
    if grid[tile[1]][tile[0]] == 0:
        color = (0, 200, 0)
    else:
        color = (200, 0, 0)
    selected_tile.fill(color)
    selected_tile.set_alpha(125)
    screen.blit(selected_tile, selected_rect)
    # pygame.draw.rect(screen, color, selected_tile)
    pygame.draw.rect(screen, (20, 20, 20, 50), selected_rect, 1)
            
#Tower functions
def place_tower(pos):
    #Create new tower
    new_tower = Tower(pos[0], pos[1], TILE_SIZE)
    #Check if tile already has tower in it
    can_place = True
    for  t in tower_list:
        if t.rect.colliderect(new_tower):
            can_place = False
            print("Can't place here!")
            break
    for e in enemy_list:
        if e.rect.colliderect(new_tower):
            can_place = False
    #only place if tile is empty
    if can_place == True:
        tower_list.append(new_tower)
        grid[new_tower.y // TILE_SIZE][new_tower.x // TILE_SIZE] = 1
        print("Tower placed!")

def select_tower(mouse_pos):
    #Clicking on tower selects it, clicking off tower deselects it
    for t in tower_list:
        if t.rect.collidepoint(mouse_pos):
            print("Tower  Clicked!")
            t.selected = not t.selected
        else:
            t.selected = False

def remove_tower(tower):
    grid[tower.y // TILE_SIZE][tower.x // TILE_SIZE] = 0
    tower_list.remove(tower)
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
                for t in tower_list:
                    if t.selected:
                        remove_tower(t)
        
            if event.key == pygame.K_c:
                if MODE == 0: MODE = 1
                else: MODE = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.__getattribute__('button') == 1:
                if MODE == 0: 
                    preview_tiles.clear()
                    dragging = True
                else: 
                    select_tower(mouse_pos)

            elif event.__getattribute__('button') == 3:
                #Cancel selection with right click while selecting
                if MODE == 0:
                    preview_tiles.clear()
                    dragging = False
                #If not building and dragging right click quick destroy
                elif MODE == 1:
                    preview_tiles.clear()
                    dragging = True     
        
        if event.type == pygame.MOUSEBUTTONUP:
            #stop selecting, place/destroy towers in building selection, and clear selection area
            dragging = False
            for tile in preview_tiles:
                    #Build towers
                    if grid[tile[1]][tile[0]] == 0 and MODE == 0:
                        place_tower((tile[0] * TILE_SIZE + TILE_SIZE // 2, tile[1] * TILE_SIZE + TILE_SIZE // 2))
                    #Destroy towers if in select mode dragging
                    if grid[tile[1]][tile[0]] == 1 and MODE == 1:
                        for t in tower_list:
                            if t.rect.collidepoint(tile[0] * TILE_SIZE + TILE_SIZE // 2, tile[1] * TILE_SIZE + TILE_SIZE // 2):
                                remove_tower(t)
            preview_tiles.clear()
    
    building_selection()
    #Draw section
    screen.fill('black')

    #draw mouse indicator and get mouse position
    mouse_position()

    #Draw grid
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[row][col] == 0:
                if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    color = (0, 100, 200)
                else:
                    color = (80, 80, 80)
            else:
                if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    color = (200, 100, 0)
                else:
                    color = (50, 50, 50)
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (20, 20, 20), rect, 1)
    
    for e in enemy_list:
        e.update()
        e.draw(screen)

    #Draw towers
    for t in tower_list:
        t.draw(screen)
    
    #draw building selection
    for tile in preview_tiles:
        draw_selection()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
'''TODO: Make Grid
highlight tile over mouse hover
different highlight colors
Make tiles toggleable between walkable and non
make towers
place towers on click
build mode
make towers selectable
make enemies
make enemies spawn on E
Make buildings
Make enemies pathfind to buildings
Combat system
'''