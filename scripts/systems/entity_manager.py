import pygame
from entity import Entity
from utils.helpers import load_image

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
        print(blueprint)

        self.entities.append(entity)
        return entity
    
    def load_entity_images(self):
        for entity in self.entities:
            if entity.rendering_component:
                entity_image = load_image(entity.rendering_component['image path'])
                entity.rendering_component['image'] = entity_image
    
    def render_entities(self, screen):
        sorted_entities = sorted(self.entities, key=lambda x: x.position[1])
        for entity in sorted_entities:
            if entity.rendering_component and entity.rendering_component['image'] != None:
                entity_image = entity.rendering_component['image']
                rect = entity_image.get_rect()
                rect.topleft = entity.position
                screen.blit(entity_image, rect)
            if entity.rendering_component['image'] == None:
                entity_image = load_image(entity.rendering_component['image path'])
                entity.rendering_component['image'] = entity_image
                
            if not entity.rendering_component['image']:
                print(f"Entity {entity.id} has no image?!?")


"""MAKE ONE SINGLE ENTITY THAT SPAWNS AND RENDERS A SQUARE

"""
