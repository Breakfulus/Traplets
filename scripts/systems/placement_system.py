import pygame
import utils.consts as c

class PlacementSystem:
    def __init__(self, grid):
        self.grid = grid
        self.preview_tiles = set()
        self.dragging = False
        self.selected_blueprint = None #What it is placing

    def mouse_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        col = mouse_x // c.TILE_SIZE
        row = mouse_y // c.TILE_SIZE
        cell_x = col * c.TILE_SIZE
        cell_y = row * c.TILE_SIZE
        center_x = cell_x + c.TILE_SIZE // 2
        center_y = cell_y + c.TILE_SIZE // 2
        return center_x, center_y

    def building_selection(self):
        mouse_pos = self.mouse_position()
        #drag selecting
        if self.dragging:
            tile_x, tile_y = mouse_pos[0] // c.TILE_SIZE, mouse_pos[1] // c.TILE_SIZE
            if 0 <= tile_x < c.GRID_WIDTH and 0 <= tile_y < c.GRID_HEIGHT:
                self.preview_tiles.add((tile_x, tile_y))
                print(self.preview_tiles)
    
    def place(self, tile_pos, group):
        if self.selected_blueprint == None:
            return
        row, col = tile_pos

        if not self.grid.is_empty(row, col):
            return
        
        world_x = col * c.TILE_SIZE
        world_y = row * c.TILE_SIZE

        new_obj = self.selected_blueprint(world_x, world_y, c.TILE_SIZE // 2)

        group.add(new_obj)
        self.grid.set_tile(row, col, 1)

    def finalize_placement(self, group):
        for tile in self.preview_tiles:
            self.place((tile[1], tile[0]), group)
        self.preview_tiles.clear()
        self.dragging = False

    def draw_selection(self, surf):
        for tile in self.preview_tiles:
            selected_rect = pygame.Rect(tile[0] * c.TILE_SIZE, tile[1] * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE)
            selected_tile  = pygame.Surface((c.TILE_SIZE, c.TILE_SIZE))
            if self.grid.is_empty(tile[1],tile[0]):
                color = (0, 200, 0)
            else:
                color = (200, 0, 0)
            selected_tile.fill(color)
            selected_tile.set_alpha(125)
            surf.blit(selected_tile, selected_rect)
            pygame.draw.rect(surf, (20, 20, 20, 50), selected_rect, 1)
    
    def draw(self, surf):
        self.draw_selection(surf)