import pygame
from entity import Entity
from utils.helpers import load_image
import utils.consts as c


class EntityManager:
    def __init__(self, grid):
        self.entities = {}
        self.enemies = {}
        self.towers = {}
        self.projectiles = {}
        self.grid = grid

    def create_entity(self, blueprint, pos, tiles, team, eid=None):

        # only reserve and ID if entity isn't already given one before creation
        if eid == None:
            eid = Entity.reserve_id()

        entity = Entity(pos, team, eid)

        for comp_name, comp_stats in blueprint.items():
            setattr(entity, comp_name, comp_stats.copy())

        self.entities[eid] = entity

        if entity.need["type"] == "enemy":
            self.enemies[eid] = entity

        if entity.need["type"] == "tower":
            self.towers[eid] = entity

        if entity.need["type"] == "projectile":
            self.projectiles[eid] = entity

        entity.grid_pos = [
            entity.position[1] // c.TILE_SIZE,
            entity.position[0] // c.TILE_SIZE,
        ]
        row, col = entity.grid_pos
        print(f"Entity {entity.id} tile pos: {entity.grid_pos}!")

        layer = entity.need["layer"]

        for row, col in tiles:
            self.grid.add_to_tile(row, col, layer, eid)

        self.load_entity_images(entity)
        print(f"Entity {entity.id} has been created!")
        print(self.enemies)
        return entity

    def entity_clean_up(self):
        for eid, entity in self.entities.items():
            if not entity.alive:
                # remove all of that entity from the grid
                for r in range(self.grid.grid_height):
                    for c_ in range(self.grid.grid_width):
                        if eid in self.grid.get_tile(r, c_, entity.need["layer"]):
                            self.grid.remove_from_tile(r, c_, entity.need["layer"], eid)
                # actually remove the entity
                del self.entities[eid]
                return

    def load_entity_images(self, entity):
        if entity.rendering_component:
            entity_image = load_image(entity.rendering_component["image path"])
            entity.rendering_component["image"] = entity_image

    def render_entities(self, screen):
        sorted_entities = sorted(self.entities.values(), key=lambda y: y.position[1])
        for entity in sorted_entities:
            if (
                entity.rendering_component
                and entity.rendering_component["image"] != None
            ):
                entity_image = entity.rendering_component["image"]
                rect = entity_image.get_rect()
                entity.rendering_component["image_rect"] = rect
                rect.center = entity.position
                screen.blit(entity_image, rect)

        for entity in sorted_entities:
            if hasattr(entity, "structure_component"):
                if hasattr(entity, "combat_component"):
                    if entity.structure_component["selectable"]:
                        if entity.structure_component.get("selected"):
                            pygame.draw.circle(
                                screen,
                                "red",
                                entity.rendering_component.get("image_rect").center,
                                entity.combat_component["range"] * c.TILE_SIZE,
                                5,
                            )

                    if not entity.combat_component.get("targets"):
                        print("No target!")
                        continue

                    target = entity.combat_component["targets"][0]
                    tower_pos = entity.position[0], entity.position[1]
                    targ_pos = target.position[0], target.position[1]
                    pygame.draw.line(screen, "green", tower_pos, targ_pos, 5)
                    if not entity.rendering_component["image"]:
                        print(f"Entity {entity.id} has no image!")

    def select_entity(self, eid):
        for entity_id, entity in self.entities.items():
            if hasattr(entity, "structure_component"):
                entity.structure_component["selected"] = False
        if eid != None:
            entity = self.entities[eid]
            entity.structure_component["selected"] = True
