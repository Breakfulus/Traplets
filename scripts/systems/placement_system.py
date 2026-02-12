import pygame

class Grid:
    def __init__(self, grid_height, grid_width, tile_size):
        
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.tile_size = tile_size
        self.grid = [
                    [0 for _ in range(self.grid_width)]
                    for _ in range(self.grid_height)
                ]
    
    def is_empty(self, row, col):
        return self.grid[row][col] == 0
    
    def set_tile(self, row, col, value):
        self.grid[row][col] = value
    
    def get_mouse_tile_pos(self, pos):
        col = pos[0] // self.tile_size
        row = pos[1] // self.tile_size
        self.mouse_pos = (col * self.tile_size, row * self.tile_size)
        return row, col

    def draw_grid(self, screen):
    #Draw grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                if rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                    if self.is_empty(row, col):
                        color = (0, 100, 200)
                    else:
                        color = (200, 100, 0)
                else:
                    if self.is_empty(row, col):
                        color = (80, 80, 80)
                    else:
                        color = (50, 50, 50)
                
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (20, 20, 20), rect, 1)

        