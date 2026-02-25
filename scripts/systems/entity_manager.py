import pygame
from scripts.entity import Entity

class EntityManager:
    def __init__(self):
        self.entities = []

    def create_entity(self, blueprint, pos):
        entity = Entity(pos, None)
        self.entities.append(entity)

"""TODO:
make entities recieve components based on their blueprints
add entity teams
make deletion
make rendering

"""
