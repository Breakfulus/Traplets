import pygame
from tower import Tower
from enemy import Enemy

pygame.init()

GRID_WIDTH = 5
GRID_HEIGHT = 5
TILE_SIZE = 64
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
GRAY = (15, 15, 15)
MODE = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Traplet Tower Defense")

clock = pygame.time.Clock()

path = [(0 * TILE_SIZE + TILE_SIZE // 2, 0 * TILE_SIZE + TILE_SIZE // 2)]
#hold tower position and data
tower_list = []

grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

new_enemy = Enemy(0, 0, TILE_SIZE / 2, path, 100, 2, 100, 100, 0)

def mouse_position(): #get position of the tile mouse is hopvering over and indicate where the tower is placed
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col = mouse_x // TILE_SIZE
    row = mouse_y // TILE_SIZE
    cell_x = col * TILE_SIZE
    cell_y = row * TILE_SIZE
    center_x = cell_x + TILE_SIZE // 2
    center_y = cell_y + TILE_SIZE // 2
    return center_x, center_y

#Tower functions
def place_tower(mouse_pos):
    #Create new tower
    new_tower = Tower(mouse_pos[0], mouse_pos[1], TILE_SIZE)
    #Check if tile already has tower in it
    can_place = True
    for  t in tower_list:
        if t.rect.colliderect(new_tower):
            can_place = False
            print("Can't place here!")
            break

    #only place if tile is empty
    if can_place == True:
        tower_list.append(new_tower)
        print("Tower placed!")

def select_tower(mouse_pos):
    #Clicking on tower selects it, clicking off tower deselects it
    for t in tower_list:
        if t.rect.collidepoint(mouse_pos):
            print("Tower  Clicked!")
            t.selected = not t.selected
        else:
            t.selected = False

def remove_tower():
    for t in tower_list:
        if t.selected:
            tower_list.remove(t)
            print("Tower removed!")




running = True
while running:
    mouse_pos = mouse_position()

    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                remove_tower()
        
            if event.key == pygame.K_c:
                if MODE == 0: MODE = 1
                else: MODE = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if MODE == 0: 
                tile_x, tile_y = mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE #get the tile the mouse is over
                if grid[tile_y][tile_x] == 0: #if the tile is empty place a tower
                    place_tower(mouse_pos)

            else: 
                select_tower(mouse_pos)

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

    #Draw towers
    for t in tower_list:
        t.draw(screen)
    
    new_enemy.update()
    new_enemy.draw(screen)
    
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