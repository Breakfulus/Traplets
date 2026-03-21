import pygame
import utils.consts as c
from utils.entity_definitions import TOWER_DEFINITIONS
from entity import Entity

PLACETOWER = pygame.USEREVENT + 1
DESTROYTOWER = pygame.USEREVENT + 2
SELECTTOWER = pygame.USEREVENT + 3

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
        self.footprint = self.selected_blueprint['structure_component']['footprint']

        for r in range(len(self.footprint)):
            for c_ in range(len(self.footprint[r])):

                if self.footprint[r][c_] == 0:
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
        
        entity_id = Entity.reserve_id()
        
        world_x = start_col * c.TILE_SIZE
        world_y = start_row * c.TILE_SIZE
        place_tower_event = pygame.event.Event(PLACETOWER, pos=(world_x, world_y), blueprint=self.selected_blueprint, team='player', eid=entity_id)
        pygame.event.post(place_tower_event)

        for r in range(len(self.footprint)):
            for c_ in range(len(self.footprint[r])):
                if self.footprint[r][c_] == 0:
                    continue
            
                grid_row = start_row + r
                grid_col = start_col + c_
                self.grid.set_tile(grid_row, grid_col, entity_id)
    
    def destroy(self, row, col, tile):
        obj = self.grid.get_tile(tile[1], tile[0])
        if obj and obj != None:
            destroy_tower_event = pygame.event.Event(DESTROYTOWER, eid=obj)
            pygame.event.post(destroy_tower_event)

        for r in range(self.grid.grid_height):
            for c_ in range(self.grid.grid_width):
                if self.grid.get_tile(r, c_) == obj:
                    self.grid.set_tile(r, c_, None)
        
    def finalize_destruction(self):
        for tile in self.preview_tiles:
            self.destroy(tile[0], tile[1], tile)
            

        self.preview_tiles.clear()
        self.dragging = False
        
    def finalize_placement(self):
        for tile in self.preview_tiles:
            self.place(tile[1], tile[0])
        print(self.grid.grid)
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

    def placement_system_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.__getattribute__('button') == 1:
                if c.MODE == 0: 
                    self.preview_tiles.clear()
                    self.dragging = True
                else: 
                    self.preview_tiles.clear()
                    self.dragging = False
                    mouse_pos = pygame.mouse.get_pos()
                    tile_clicked = mouse_pos[0] // c.TILE_SIZE, mouse_pos[1] // c.TILE_SIZE
                    print(f"Tile: {tile_clicked}")

                    tile_id = self.grid.get_tile(tile_clicked[1], tile_clicked[0])
                    select_tower_event = pygame.event.Event(SELECTTOWER, eid=tile_id)
                    print(tile_id)
                    pygame.event.post(select_tower_event)

            elif event.__getattribute__('button') == 3:
                #Cancel selection with right click while selecting
                if c.MODE == 0:
                    self.preview_tiles.clear()
                    self.dragging = False

                #If not building and dragging right click quick destroy
                elif c.MODE == 1:
                    self.preview_tiles.clear()
                    self.dragging = True     
        
        if event.type == pygame.MOUSEBUTTONUP:
            if c.MODE == 0:
                self.finalize_placement()
            else:
                self.finalize_destruction()

            self.preview_tiles.clear()