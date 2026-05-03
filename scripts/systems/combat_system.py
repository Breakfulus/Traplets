import pygame
from utils import consts as c
from utils.entity_definitions import *
import math
from utils.geometry import *
from utils.attacks import ATTACKS

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
        

        for id in ids:
            if id not in self.manager.entities.keys():
                ids.remove(id)
        
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

            attack_type = entity.combat_component['type']
            entity.combat_component['func'] = ATTACKS[attack_type]
            attack_func = entity.combat_component['func']

            attack_func(entity, target, 
                        self.manager.create_entity(
                PROJECTILE_DEFINITIONS['template'],
                (entity.position[0], entity.position[1]),
                [(0, 0)],
                entity.team,
                eid=None
            ))
        
            entity.combat_component['last_shot'] = now


    
    def move_projectiles(self):
        for eid, proj in self.manager.projectiles.items():
            velocity = proj.velocity_component['velocity']
            proj.position[0] += velocity[0]
            proj.position[1] += velocity[1]
    
    def apply_damage(self, projectile, target):
        now = pygame.time.get_ticks()
        if now - target.combat_component['last_hit'] >= .5*1000: #Invincibility time; prevents entities from getting hit by same proj twice

            target.health_component['health'] -= projectile.damage_component['damage']

            target.combat_component['last_hit'] = now #reset incibility reference
        
        if target.health_component['health'] <= 0: #kill entity if its health is 0
            target.alive = False
        
    def get_projectile_hits(self):
        for projectile in self.manager.projectiles.values():
            for entity in self.manager.entities.values(): #goes through all entities for every projectile

                if entity == projectile: #projectile cant hit projectiles
                    continue

                if entity.team == projectile.team: #no friendly fire
                    continue
                
                if circle_collision(projectile.position, projectile.collision_component['collider'], entity.position, entity.collision_component['collider']):
                    #apply damage before killing the projectile so projectiles with pierce arent destroyed by dead entity
                    self.apply_damage(projectile, entity)

                    if projectile.peirce_component['peirce'] != 0: #dont kill projectile if it can hit multiple entities
                        projectile.peirce_component['peirce'] -= 1
                    else:
                        projectile.alive = False

                    

    def update(self, grid, entities):
            
            self.move_projectiles()

            self.get_projectile_hits()

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
