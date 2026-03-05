import pygame
import utils.consts as c
from utils.entity_definitions import TOWER_DEFINITIONS

PLACETOWER = pygame.USEREVENT + 1

class PlacementSystem:
    def __init__(self, grid):
        self.grid = grid
        self.preview_tiles = set()
        self.dragging = False
        self.selected_blueprint = TOWER_DEFINITIONS['mushant'] #What it is placing

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
    
    def can_place(self, start_row, start_col):
        for comp_name, comp_stats in self.selected_blueprint.items():
            if comp_name == 'placement_component':
                tower_placement_comp = comp_stats
                for stat_name, stat in tower_placement_comp.items():
                    if stat_name == 'footprint':
                        footprint = stat

        self.footprint = self.selected_blueprint['placement_component']
        self.footprint = self.footprint['footprint']

        for r in range(len(self.footprint)):
            for c_ in range(len(self.footprint[r])):

                if self.footprint[r][c_] != 1:
                    continue
            
                grid_row = start_row + r
                grid_col = start_col + c_

                if grid_row < 0 or grid_row >= c.GRID_HEIGHT:
                    return False
                if grid_col < 0 or grid_col >= c.GRID_WIDTH:
                    return False
                
                if not self.grid.is_empty(grid_row, grid_col):
                    return False
        return True


    def place(self, start_row, start_col):
        if self.selected_blueprint == None:
            return

        if not self.can_place(start_row, start_col):
            return
        
        world_x = start_col * c.TILE_SIZE
        world_y = start_row * c.TILE_SIZE
        place_tower_event = pygame.event.Event(PLACETOWER, pos=(world_x, world_y), blueprint=self.selected_blueprint, team='player')
        pygame.event.post(place_tower_event)

        for r in range(len(self.footprint)):
            for c_ in range(len(self.footprint[r])):
                if self.footprint[r][c_] != 1:
                    continue
            
                grid_row = start_row + r
                grid_col = start_col + c_
                self.grid.set_tile(grid_row, grid_col, 1)
    
    def destroy(self, row, col):
        obj = self.grid.get_tile(row, col)
        if not obj:
            return
        print(obj)
        obj.alive = False
        for r in range(self.grid.grid_height):
            for c_ in range(self.grid.grid_width):
                if self.grid.get_tile(r, c_) == obj:
                    self.grid.set_tile(r, c_, 0)
        
        
    def finalize_destruction(self):
        for tile in self.preview_tiles:
            self.destroy(tile[0], tile[1])
        self.preview_tiles.clear()
        self.dragging = False

    def finalize_placement(self):
        for tile in self.preview_tiles:
            self.place(tile[1], tile[0])
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