import pygame

class Entity:
    __next_id__ = 0

    @classmethod
    def reserve_id(cls):
        entity_id = cls.__next_id__
        cls.__next_id__ += 1
        return entity_id
        
    def __init__(self, position, team, eid=None):
        self.id = eid

        self.position = list(position)
        self.team = team
        self.type = None
        self.alive = True