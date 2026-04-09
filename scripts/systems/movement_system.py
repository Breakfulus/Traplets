import pygame
import utils.consts as c

class MovementSystem:
    def __init__(self):
        pass 
    
    def update_entity_grid_pos(self, grid, entity):
        new_col = round(entity.position[0] // c.TILE_SIZE)
        new_row = round(entity.position[1] // c.TILE_SIZE)
        if (new_col, new_row) != entity.grid_pos:
            old_col, old_row = entity.grid_pos

            entity_id = entity.id

            grid.remove_from_tile(old_col, old_row, c.ENEMIES, entity_id)
            grid.add_to_tile(new_col, new_row, c.ENEMIES, entity.id)

        entity.grid_pos = (new_col, new_row)
        print(grid.get_tile(new_col, new_row, c.ENEMIES))
        print(f"Entity {entity.id} moved to {entity.grid_pos}!")


    def move_towards_target(self, entity, movement):
        if not movement['path'] or movement['path'] == None: #Do nothing if the target doesnt have a set path
            return

        speed = movement['speed']
        path = movement['path']
        target = movement['target_index']

        if target != None: 
            #move if the target has more points in its path
            target_waypoint = path[target]
            dx  = target_waypoint[0] - entity.position[0]
            dy = target_waypoint[1] - entity.position[1]

            distance = (dx ** 2 + dy ** 2) ** .5

            if distance <= speed: 
                #snap enemy to next point if theyre close enough
                entity.position = [target_waypoint[0], target_waypoint[1]]
                movement['target_index'] += 1
                if movement['target_index'] >= len(path):
                    movement['path'] = None
                    movement['goal'] = None
                    movement['needs_path'] = True
                return
            #move on x axis before y axis
            if distance != 0:
                dx /= distance
                dy /= distance
            entity.position[0] += dx *speed 
            entity.position[1] += dy * speed 


    def update(self, entities, grid, surf):
        for entity in entities.values():
            movement = getattr(entity, "movement_component", None) #get the targets movement component
            self.move_towards_target(entity, movement)
            if not movement['needs_path']:
                debug_path = []
                for (x, y) in entity.movement_component["path"]:
                    x += c.TILE_SIZE // 2
                    y += c.TILE_SIZE // 2
                    debug_path.append((x, y))
                pygame.draw.lines(surf, 'blue', False, debug_path, 5)
            

            self.update_entity_grid_pos(grid, entity)