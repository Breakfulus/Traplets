import pygame
from utils import consts as c
from utils.entity_definitions import *
import math

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
    
    def attack(self, entity, grid, cooldown):

        now = pygame.time.get_ticks()

        if now - entity.combat_component['last_shot'] >= cooldown:

            if not entity.combat_component['targets']:
                return

            target = entity.combat_component['targets'][0]

            dx = target.position[0] - entity.position[0]
            dy = target.position[1] - entity.position[1]

            dist = math.hypot(dx, dy)
            if dist == 0:
                return
            
            dx /= dist
            dy /= dist

            projectile = self.manager.create_entity(
            PROJECTILE_DEFINITIONS['template'],
            (entity.position[0], entity.position[1]),
            [(0, 0)],
            'player',
            eid=None
        )
            speed = projectile.velocity_component['speed']

            projectile.velocity_component["velocity"] = [dx * speed, dy * speed]
            entity.combat_component['last_shot'] = now
    
    def move_projectiles(self):
        for eid, proj in self.manager.projectiles.items():
            velocity = proj.velocity_component['velocity']
            proj.position[0] += velocity[0]
            proj.position[1] += velocity[1]

    def update(self, grid, towers):
            self.move_projectiles()
            for tower in towers:

                row, col = tower.grid_pos
                range_pixels = tower.combat_component['range'] * c.TILE_SIZE

                candidates = self.get_entities_in_range(grid, row, col, tower.combat_component['range'], tower)

                tower.combat_component['targets'] = self.filter_by_exact_range(tower, candidates, range_pixels)
                print("TOWER:", tower.id)
                print("TILE:", tower.grid_pos)
                if tower.combat_component['targets'] and tower.alive:
                    self.attack(tower, grid, tower.combat_component.get('cooldown') * 1000)
