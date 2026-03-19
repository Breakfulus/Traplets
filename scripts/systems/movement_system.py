import pygame

class MovementSystem:
    def __init__(self, entity):
        self.entity = entity
        

    def move_towards_target(self):
        movement = getattr(self.entity, "movement_component", None) #get the targets movement component

        if not movement['path'] or movement['path'] == None: #Do nothing if the target doesnt have a set path
            return

        speed = movement['speed']
        path = movement['path']
        target = movement['target_index']

        if target != None: 
            print(target)
            #move if the target has more points in its path
            target_waypoint = path[target]
            dx  = target_waypoint[0] - self.entity.position[0]
            dy = target_waypoint[1] - self.entity.position[1]

            distance = (dx ** 2 + dy ** 2) ** .5

            if distance <= speed: 
                #snap enemy to next point if theyre close enough
                self.entity.position = [target_waypoint[0], target_waypoint[1]]
                movement['target_index'] += 1
                if movement['target_index'] >= len(path):
                    movement['target_index'] = len(path) - 1
                return
            #move on x axis before y axis
            if distance != 0:
                dx /= distance
                dy /= distance
            self.entity.position[0] += dx *speed 
            self.entity.position[1] += dy * speed 