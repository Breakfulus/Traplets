import pygame
from utils import consts as c
from utils.entity_definitions import *
import math
from utils.geometry import *

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
        
        print("entity tiles checked:", tiles)
        return tiles
    
    def get_entities_in_range(self, grid, row, col, radius, entity):
        tiles = self.get_tiles_in_range(row, col, radius)
        ids = []

        for r, c_ in tiles:
            ids.extend(grid.get_tile(r, c_, entity.need['target_layer']))

        print("IDS:", ids)
        
        targets = [self.manager.entities[eid] for eid in ids]
        
        print("TARGETS:", targets)
        return targets

    def filter_by_exact_range(self, entity, targets, radius):
        result = []

        for target in targets:

            if get_dist_sq(entity.position, target.position) <= radius*radius:
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
            entity.team,
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
    
    def apply_damage(self, projectile, target):
        target.health_component['health'] -= projectile.projectile_component['damage']

        if projectile.projectile_compoenent['peirce'] == 0:
            projectile.alive = False
        else:
            projectile.projectile_component['peirce'] -= 1
        
        if target.health_compoenent['health'] <= 0:
            target.alive = False
    

    def update(self, grid, entities):
            
            self.move_projectiles()
            for entity in entities:
                combat = getattr(entity, "combat_component", None)

                if not combat:
                    continue

                if entity.need['type'] != 'tower':
                    continue

                row, col = entity.grid_pos
                range_pixels = combat['range'] * c.TILE_SIZE

                candidates = self.get_entities_in_range(grid, row, col, combat['range'], entity)

                combat['targets'] = self.filter_by_exact_range(entity, candidates, range_pixels)

                print("entity:", entity.id)
                print("TILE:", entity.grid_pos)
                if combat['targets'] and entity.alive:
                    self.attack(entity, grid, combat.get('cooldown') * 1000)
