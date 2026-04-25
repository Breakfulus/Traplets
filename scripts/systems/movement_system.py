import pygame
import utils.consts as c
import math

class MovementSystem:
    def __init__(self):
        pass 
    
    def update_entity_grid_pos(self, grid, entity):
        new_col = int(entity.position[0] // c.TILE_SIZE)
        new_row = int(entity.position[1] // c.TILE_SIZE)
        if (new_row, new_col) != entity.grid_pos:

            old_row, old_col = entity.grid_pos

            entity_id = entity.id
            
            grid.add_to_tile(new_row, new_col, c.ENEMIES, entity.id)
            grid.remove_from_tile(old_row, old_col, c.ENEMIES, entity_id)

        entity.grid_pos = (new_row, new_col)
        print("Enemy actual tile:",
            int(entity.position[1] // c.TILE_SIZE),
            int(entity.position[0] // c.TILE_SIZE))


    def move_towards_target(self, entity, movement, sep_x=0, sep_y=0, sep_force=0):
        speed = movement['speed']
        path = movement['path']
        target = movement['target_index']
        
        if not path: #Do nothing if the target doesnt have a set path
            return

        if target == None or target >= len(path): 
            return
        
        #move if the target has more points in its path
        tx, ty = path[target]

        dx  = tx - entity.position[0]
        dy = ty - entity.position[1]

        distance = math.hypot(dx, dy)
        
        #move on x axis before y axis
        if distance == 0:
            movement['target_index'] += 1
            return
        
        dx /= distance
        dy /= distance
        
        vx = dx * speed
        vy = dy * speed
        vx += sep_x * sep_force
        vy += sep_y * sep_force

        entity.position[0] += vx
        entity.position[1] += vy

        if distance <= c.TILE_SIZE // 2:
            sep_force /= 2

        if distance <= speed:
            if speed > 0:
                speed-=1

            movement['target_index'] += 1

            if movement['target_index'] >= len(path):
                movement['path'] = None
                movement['goal'] = None
                movement['needs_path'] = True
                

    def separate_enemies(self, enemy, enemies):
        strength = 0
        sep_x = 0
        sep_y = 0

        for other in enemies:
            
            if other == enemy: #ignore itself
                continue
        
            #calc distance between eachother
            dx = enemy.position[0] - other.position[0]
            dy = enemy.position[1] - other.position[1]

            dist_sq = dx*dx + dy*dy
            min_dist = 25

            #if overlapping completely
            if dist_sq == 0:
                continue

            dist = math.sqrt(dist_sq)
            
            if dist <= min_dist:
                dx /= dist
                dy /= dist

                strength = 1/dist * 5

                sep_x += dx * strength
                sep_y += dy * strength
        
        return sep_x, sep_y, min_dist

    def update(self, entities, grid):
        self.grid = grid
        enemies = list(entities.values())
        for enemy in enemies:
            movement = getattr(enemy, "movement_component", None) #get the targets movement component

            if not movement["path"] or movement["path"] == None:
                continue

            if movement["path_dirty"]:
                continue
            
            # if not movement['needs_path']: #draw a debug path
            #     debug_path = []
            #     for (x, y) in enemy.movement_component["path"]:
            #         x += c.TILE_SIZE // 2
            #         y += c.TILE_SIZE // 2
            #         debug_path.append((x, y))
            #     pygame.draw.lines(surf, 'blue', False, debug_path, 5)

            sep_x, sep_y, sep_force = self.separate_enemies(enemy, enemies)

            self.move_towards_target(enemy, movement, sep_x, sep_y, sep_force)

            self.update_entity_grid_pos(grid, enemy)
