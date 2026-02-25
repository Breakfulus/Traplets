import pygame
from scripts.entity import Entity

class EntityManager:
    def __init__(self):
        self.entities = []

    def create_entity(self, blueprint, pos):
        entity = Entity(pos, None)
        self.entities.append(entity)