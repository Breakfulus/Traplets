import pygame
from utils import consts as c
from utils.entity_definitions import *
import math
from utils.geometry import *
from utils.attacks import ATTACKS
import random


class CombatSystem:
    def __init__(self, manager):
        self.manager = manager

    def get_tiles_in_range(
        self, center_row, center_col, radius
    ):  # Get tiles covered by range radius
        tiles = []
        radius_sq = radius * radius

        for row in range(center_row - radius, center_row + radius + 1):
            for col in range(center_col - radius, center_col + radius + 1):
                if row < 0 or col < 0 or row >= c.GRID_HEIGHT or col >= c.GRID_WIDTH:
                    continue

                dx = col - center_col
                dy = row - center_row

                if dx * dx + dy * dy <= radius_sq:
                    tiles.append((row, col))

        print("entity tiles checked:", tiles)
        return tiles

    def get_entities_in_range(
        self, grid, row, col, radius, entity
    ):  # Get entities from tiles covered by range radius
        tiles = self.get_tiles_in_range(row, col, radius)
        ids = []

        for r, c_ in tiles:
            ids.extend(grid.get_tile(r, c_, entity.need["target_layer"]))

        print("IDS:", ids)

        for id in ids:
            if id not in self.manager.entities.keys():
                ids.remove(id)

        targets = [self.manager.entities[eid] for eid in ids]

        print("TARGETS:", targets)
        return targets

    def filter_by_exact_range(
        self, entity, targets, radius
    ):  # Get entities in range radius
        result = []

        for target in targets:
            if get_dist_sq(entity.position, target.position) <= radius * radius:
                result.append(target)

        print("LOS RESULT:", result)
        return result

    def attack(self, entity, cooldown):

        now = pygame.time.get_ticks()

        if now - entity.combat_component["last_shot"] >= cooldown:
            if not entity.combat_component["targets"]:
                return

            # Get the attack type from the entity data
            attack_type = entity.combat_component["type"]
            entity.combat_component["func"] = ATTACKS[attack_type]
            attack_func = entity.combat_component["func"]

            # optional data for any attack to use
            context = {
                "target": entity.combat_component["targets"][0],
                "targets": entity.combat_component["targets"],
                "manager": self.manager,
                "apply_damage": self.apply_damage,
                "is_crit": entity.critical_hit_component["is_crit"],
            }

            # Call the associated attack function
            attack_func(entity, context)
            # Update the time for the most recent attack to now
            entity.combat_component["last_shot"] = now

    def is_critical_hit(self, attacker=None):
        if attacker is None:
            return False

        crit = getattr(attacker, "critical_hit_component", None)
        if crit is None:
            return

        if random.random() < crit["crit_chance"]:
            crit["is_crit"] = True

    def move_projectiles(self):
        for eid, proj in self.manager.projectiles.items():
            # Grab entity stored velocity and move the objects position with it
            velocity = proj.velocity_component["velocity"]

            proj.position[0] += velocity[0]
            proj.position[1] += velocity[1]

    def apply_damage(self, damage, target):

        now = pygame.time.get_ticks()

        if (
            now - target.health_component["last_hit"] >= 0.5 * 1000
        ):  # Invincibility time; prevents entities from getting hit by same proj twice
            target.health_component["health"] -= damage

            target.health_component["last_hit"] = (
                now  # Updates to ost recent time entity was damaged
            )

    def get_projectile_hits(self):
        for projectile in self.manager.projectiles.values():
            for entity in (
                self.manager.entities.values()
            ):  # goes through all entities for every projectile
                if (
                    entity.need["type"] == "projectile"
                ):  # projectile cant hit projectiles
                    continue

                if entity.team == projectile.team:  # no friendly fire
                    continue

                if circle_collision(
                    projectile.position,
                    projectile.collision_component["collider"],
                    entity.position,
                    entity.collision_component["collider"],
                ):
                    if (
                        projectile.peirce_component["peirce"] != 0
                    ):  # dont kill projectile if it can hit multiple entities
                        projectile.peirce_component["peirce"] -= 1
                    else:
                        projectile.alive = False

                    self.apply_damage(projectile.damage_component["damage"], entity)

    def despawn_projectiles(self):
        for projectile in self.manager.projectiles.values():
            despawn = getattr(projectile, "despawn_component", None)

            if not despawn:
                return

            if despawn["time_alive"] != despawn["lifespan"]:
                despawn["time_alive"] += 0.001

            elif despawn["time_alive"] >= despawn["lifespan"]:
                projectile.alive = False

    def kill_entities(self, entities):
        for entity in entities:
            health = getattr(entity, "health_component", None)

            if health:
                if health["health"] != 0:
                    continue

                if entity.need["type"] == "base":
                    c.GAME_STATE = 1

                entity.alive = False

    def update(self, grid, entities):
        self.kill_entities(entities)

        self.move_projectiles()

        self.get_projectile_hits()

        self.despawn_projectiles()

        for entity in entities:
            combat = getattr(entity, "combat_component", None)

            if not combat:
                continue

            row, col = entity.grid_pos
            range_pixels = combat["range"] * c.TILE_SIZE

            candidates = self.get_entities_in_range(
                grid, row, col, combat["range"], entity
            )

            combat["targets"] = self.filter_by_exact_range(
                entity, candidates, range_pixels
            )

            print("entity:", entity.id)
            print("TILE:", entity.grid_pos)
            if combat["targets"] and entity.alive:
                self.is_critical_hit(entity)
                self.attack(entity, combat.get("cooldown") * 1000)
