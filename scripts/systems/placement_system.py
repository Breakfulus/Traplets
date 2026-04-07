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
            col, row = mouse_pos[0] // c.TILE_SIZE, mouse_pos[1] // c.TILE_SIZE
            if 0 <= col < c.GRID_WIDTH and 0 <= row < c.GRID_HEIGHT:
                self.preview_tiles.add((col, row))
                print(self.preview_tiles)

    def place(self, start_row, start_col, tiles):
        
        entity_id = Entity.reserve_id()
        
        world_x = start_col * c.TILE_SIZE
        world_y = start_row * c.TILE_SIZE
        
        place_tower_event = pygame.event.Event(PLACETOWER, pos=(world_x, world_y), tiles=tiles, blueprint=self.selected_blueprint, team='player', eid=entity_id)
        
        if self.selected_blueprint == None:
            return
        
        pygame.event.post(place_tower_event)
    
    def destroy(self, row, col, tile):
        obj = self.grid.get_tile(tile[1], tile[0], c.STRUCTURES)
        if obj and obj != None:
            destroy_tower_event = pygame.event.Event(DESTROYTOWER, eid=obj[0])
            pygame.event.post(destroy_tower_event)
        
    def finalize_destruction(self):
        for tile in self.preview_tiles:
            self.destroy(tile[0], tile[1], tile)
            

        self.preview_tiles.clear()
        self.dragging = False
        
    def finalize_placement(self):
        reserved = set()
        for tile in sorted(self.preview_tiles, key=lambda t: (t[1], t[0])):
            footprint = self.selected_blueprint['structure_component']['footprint']
            tiles = []
            
            #build the footprint
            for r in range(len(footprint)):
                for c_ in range(len(footprint[r])):
                    if footprint[r][c_] == 0:
                        continue
                
                    grid_row = tile[1] + r
                    grid_col = tile[0] + c_
                    tiles.append((grid_row, grid_col))

            can_place = True
            for row, col in tiles:
                if not self.grid.is_not_blocked(row, col) or (row, col) in reserved:
                    can_place = False
                    break
            
            if not can_place:
                continue
            
            #reserve tile going to be occupied before placing
            for t in tiles:
                reserved.add(t)

            self.place(tile[1], tile[0], tiles)

        print(self.grid.grid)
        self.preview_tiles.clear()
        self.dragging = False

    # def finalize_placement(self):
    #     reserved = set()

    #     for tile in sorted(self.preview_tiles, key=lambda t: (t[1], t[0])):
    #         start_row, start_col = tile[1], tile[0]

    #         # build footprint tiles
    #         footprint_tiles = []
    #         for r in range(len(self.selected_blueprint['structure_component']['footprint'])):
    #             for c_ in range(len(self.selected_blueprint['structure_component']['footprint'][r])):
    #                 if self.selected_blueprint['structure_component']['footprint'][r][c_] == 0:
    #                     continue
    #                 footprint_tiles.append((start_row + r, start_col + c_))

    #         # 🔥 CHECK BOTH GRID + RESERVED
    #         can_place = True
    #         for row, col in footprint_tiles:
    #             if not self.grid.is_not_blocked(row, col) or (row, col) in reserved:
    #                 can_place = False
    #                 break

    #         if not can_place:
    #             continue

    #         # reserve tiles FIRST
    #         for t in footprint_tiles:
    #             reserved.add(t)

    #         # then place (which updates grid)
    #         self.place(start_row, start_col, footprint_tiles)

    #     self.preview_tiles.clear()
    #     self.dragging = False

    def draw_selection(self, surf):
        for tile in self.preview_tiles:
            selected_rect = pygame.Rect(tile[0] * c.TILE_SIZE, tile[1] * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE)
            selected_tile  = pygame.Surface((c.TILE_SIZE, c.TILE_SIZE))
            if self.grid.is_not_blocked(tile[1],tile[0]):
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

                    tile_id = self.grid.select_entity_in_tile(tile_clicked[1], tile_clicked[0], c.STRUCTURES)
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