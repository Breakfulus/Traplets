import pygame
import utils.consts as c

class PlacementSystem:
    def __init__(self, grid):
        self.grid = grid
        preview_tiles = set()
        self.dragging = False
        MODE = 0

    def mouse_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        col = mouse_x // c.TILE_SIZE
        row = mouse_y // c.TILE_SIZE
        cell_x = col * c.TILE_SIZE
        cell_y = row * c.TILE_SIZE
        center_x = cell_x + c.TILE_SIZE // 2
        center_y = cell_y + c.TILE_SIZE // 2
        return center_x, center_y
