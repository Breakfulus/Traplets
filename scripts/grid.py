import pygame
import utils.consts as c


class Grid:
    def __init__(self, grid_height, grid_width, tile_size):
        self.hovered_tile = (0, 0)
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.tile_size = tile_size
        self.grid = [
                    [{c.STRUCTURES: [], c.ENEMIES: [], c.PROJECTILES: []} for _ in range(self.grid_width)]
                    for _ in range(self.grid_height)
                ]
    
    #check if tile has a structure
    def is_not_blocked(self, row, col):
        tile = self.grid[row][col]
        return tile[c.STRUCTURES] == []

    #get all entities from a specific layer on the tile
    def get_tile(self, row, col, layer):
        return self.grid[row][col][layer]
    
    def select_entity_in_tile(self, row, col, layer, mouse_pos=None):
        tile = self.get_tile(row,col, layer)
        
        if not tile:
            return None
        
        if mouse_pos == None:
            return tile[0]

    def add_to_tile(self, row, col, layer, eid):
        tile = self.grid[int(row)][int(col)]
        tile[layer].append(eid)
    
    def remove_from_tile(self, row, col, layer, eid):
        for eid in self.grid[row][col][layer]:
            self.grid[row][col][layer].remove(eid)
    
    def get_mouse_tile_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        col = mouse_x // c.TILE_SIZE
        row = mouse_y // c.TILE_SIZE
        cell_x = col * c.TILE_SIZE
        cell_y = row * c.TILE_SIZE
        self.hovered_tile = (cell_x, cell_y)
        return row, col

    def draw_grid(self, screen):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                if rect.collidepoint(self.hovered_tile[0], self.hovered_tile[1]):
                    if self.is_not_blocked(row, col):
                        color = (0, 100, 200)
                    else:
                        color = (200, 100, 0)
                else:
                    if self.is_not_blocked(row, col):
                        color = (80, 80, 80)
                    else:
                        color = (50, 50, 50)
                
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (20, 20, 20), rect, 1)
    
    def update(self):
        self.get_mouse_tile_pos()

        