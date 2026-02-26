import pygame
from entity import Entity

class EntityManager:
    def __init__(self):
        self.entities = []

    def create_entity(self, blueprint, pos, team):
        entity = Entity(pos, team)
        for comp_name, comp_stats in blueprint.items():
            if hasattr(entity, comp_name):
                setattr(entity, comp_name, comp_stats.copy())
            else:
                print(f"Warning! Entity {entity.id} has no attribute {comp_name}!")

        self.entities.append(entity)
        return entity
    
    def render_entities(screen):
        for entity in self.entities:
            if entity.rendering_component:
                screen.blit(entity.rendering_component.image, entity.rendering_component.image_rect)


"""MAKE ONE SINGLE ENTITY THAT SPAWNS AND RENDERS A SQUARE

"""
