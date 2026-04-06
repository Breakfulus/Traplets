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
    
    def is_not_blocked(self, row, col):
        tile = self.grid[row][col]
        return tile[c.STRUCTURES] == []
    
    def can_place(self, start_row, start_col, footprint):

        for r in range(len(footprint)):
            for c_ in range(len(footprint[r])):

                if footprint[r][c_] == 0:
                    continue
            
                grid_row = start_row + r
                grid_col = start_col + c_

                if grid_row < 0 or grid_row >= c.GRID_HEIGHT:
                    return False
                if grid_col < 0 or grid_col >= c.GRID_WIDTH:
                    return False
                
                if not self.is_not_blocked(grid_row, grid_col):
                    return False
        return True

    def get_tile(self, row, col, layer):
        return self.grid[row][col][layer]
    
    def select_entity_in_tile(self, row, col, layer, mouse_pos=None):
        tile = self.get_tile(row,col, layer)
        
        if not tile:
            return None
        
        if mouse_pos == None:
            return tile[0]

    
    def add_to_tile(self, row, col, layer, eid):
        tile = self.grid[row][col]
        tile[layer].append(eid)
    
    def remove_from_tile(self, row, col, layer, eid):
        for eid in self.grid[row][col][layer]:
            self.grid[row][col][layer].remove(eid)
    
    def get_mouse_tile_pos(self, pos):
        col = pos[0] // self.tile_size
        row = pos[1] // self.tile_size
        self.hovered_tile = (col * self.tile_size, row * self.tile_size)
        return row, col

    def draw_grid(self, screen):
    #Draw grid
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

        