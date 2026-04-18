import pygame
from utils import consts as c

class CombatSystem:
    def __init__(self, manager):
        self.manager = manager

    def get_tiles_in_range(self, center_row, center_col, radius):
        tiles = []
        radius_sq = radius * radius

        for row in range(center_row - radius, center_row + radius + 1):
            for col in range(center_col - radius, center_col + radius + 1):

                if row < 0 or col < 0 or row >= c.GRID_HEIGHT or col >= c.GRID_WIDTH:
                    continue
                
                #calculate distance
                dx = col - center_row
                dy = row - center_row

                #check if tile is in range then add it to tiles
                if dx*dx + dy*dy <= radius_sq:
                    tiles.append((row, col))

        return tiles
    
    def get_entities_in_range(self, grid, row, col, radius):
        tiles = self.get_tiles_in_range(row, col, radius)
        ids = []

        for r, c_ in tiles:
            ids.extend(grid.get_tile(r, c_, c.ENEMIES))
        
        targets = [self.manager.entities[eid] for eid in ids]
        
        return targets

    def filter_by_exact_range(self, entity, targets, radius):
        radius_sq = radius * radius
        result = []

        for target in targets:
            dx = target.position[0] - entity.position[0]
            dy = target.position[1] - entity.position[1]

            if dx*dx + dy*dy <= radius*radius:
                result.append(target)
        
        return result
    
    def update(self, grid, towers, screen):
        for eid, tower in towers.items():
            print(tower)
            col, row = tower.grid_pos
            range_pixels = tower.combat_component['range'] * c.TILE_SIZE

            candidates = self.get_entities_in_range(grid, row, col, tower.combat_component['range'])

            targets = self.filter_by_exact_range(tower, candidates, range_pixels)
            
            for t in targets:
                tower_pos = tower.position[0] + c.TILE_SIZE // 2, tower.position[1] + c.TILE_SIZE // 2
                targ_pos = t.position[0] + c.TILE_SIZE // 2, t.position[1] + c.TILE_SIZE // 2
                pygame.draw.line(screen, 'green', tower_pos, targ_pos, 5)