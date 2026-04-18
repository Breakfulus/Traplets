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
                
                dx = col - center_col
                dy = row - center_row

                if dx*dx + dy*dy <= radius_sq:
                    tiles.append((row, col))
        print("Tower tiles checked:", tiles)
        return tiles
    
    def get_entities_in_range(self, grid, row, col, radius, entity):
        tiles = self.get_tiles_in_range(row, col, radius)
        ids = []

        for r, c_ in tiles:
            ids.extend(grid.get_tile(r, c_, c.ENEMIES))

        print("IDS:", ids)
        
        targets = [self.manager.entities[eid] for eid in ids]
        
        print("TARGETS:", targets)
        return targets

    def filter_by_exact_range(self, entity, targets, radius):
        radius_sq = radius * radius
        result = []

        for target in targets:
            dx = target.position[0] - entity.position[0]
            dy = target.position[1] - entity.position[1]

            print("DISTANCES:", [(dx*dx + dy*dy, "vs", radius_sq)])

            if dx*dx + dy*dy <= radius_sq:
                result.append(target)

        print("LOS RESULT:", result)
        return result
    
    def update(self, grid, towers):
        for eid, tower in towers.items():
            print("TOWER:", tower.id)
            print("TILE:", tower.grid_pos)
            row, col = tower.grid_pos
            range_pixels = tower.combat_component['range'] * c.TILE_SIZE

            candidates = self.get_entities_in_range(grid, row, col, tower.combat_component['range'], tower)

            tower.combat_component['targets'] = self.filter_by_exact_range(tower, candidates, range_pixels)