import pygame

class MovementSystem:
    def __init__(self):
        pass
        
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

    def update(self, entities):
        for entity in entities.values():
            movement = getattr(entity, "movement_component", None) #get the targets movement component
            self.move_towards_target(entity, movement)