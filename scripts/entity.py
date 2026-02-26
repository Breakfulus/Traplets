import pygame

class Entity:
    __next_id__ = 0
    def __init__(self, position, team):
        self.id = Entity.__next_id__
        Entity.__next_id__ += 1

        self.position = position
        self.team = team
        self.type = None

        #component block
        self.placement_component = None
        self.movement_component = None
        self.rendering_component = None