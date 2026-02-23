import pygame

class Entity:
    __next_id__ = 0
    def __init__(self, position, team):
        self.id = Entity.__next_id__
        Entity.__next_id__ += 1

        self.position = position
        self.team = team
        self.type = entity_type

        #component block
        placement_component = None
        movement_component = None
        rendering_component = None