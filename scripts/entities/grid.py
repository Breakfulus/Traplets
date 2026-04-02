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

    def get_tile(self, row, col, layer):
        return self.grid[row][col][layer]
    
    def add_to_tile(self, row, col, layer, entity):
        tile = self.grid[row][col]
        tile[layer].append(entity)
    
    def remove_from_tile(self, row, col, layer, entity):
        for entity in self.grid[row][col][layer]:
            self.grid[row][col][layer].remove(entity)
    
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

        