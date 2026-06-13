import pygame
import utils.consts as c
import math
from utils.geometry import *


class MovementSystem:
    def __init__(self):
        pass

    def update_entity_grid_pos(self, grid, entity):
        new_col = int(entity.position[0] // c.TILE_SIZE)
        new_row = int(entity.position[1] // c.TILE_SIZE)
        if (new_row, new_col) != entity.grid_pos:
            old_row, old_col = entity.grid_pos

            entity_id = entity.id

            grid.add_to_tile(new_row, new_col, c.ENEMIES, entity.id)
            grid.remove_from_tile(old_row, old_col, c.ENEMIES, entity_id)

        entity.grid_pos = (new_row, new_col)
        # print("Enemy actual tile:",
        #     int(entity.position[1] // c.TILE_SIZE),
        #     int(entity.position[0] // c.TILE_SIZE))

    def move_towards_target(
        self,
        entity,
        movement,
        sep_force=(0, 0),
        knockback_force=0,
        collision_force=(0, 0),
    ):
        speed = movement["speed"]
        path = movement["path"]
        target = movement["target_index"]

        if not path:  # Do nothing if the target doesnt have a set path
            return

        if target is None or target >= len(path):
            return

        # move if the target has more points in its path
        tx, ty = path[target]

        dx = tx - entity.position[0]
        dy = ty - entity.position[1]

        distance = math.hypot(dx, dy)

        # move on x axis before y axis
        if distance == 0:
            movement["target_index"] += 1
            return

        col_x, col_y = collision_force
        sep_x, sep_y = sep_force

        dx /= distance
        dy /= distance

        vx = dx * speed
        vy = dy * speed
        vx += sep_x + col_x
        vy += sep_y + col_y

        # gradually dampen velocity
        vx *= 0.9
        vy *= 0.9

        entity.position[0] += vx
        entity.position[1] += vy

        # cap velocity
        max_speed = 3

        speed = math.sqrt(vx * vx + vy * vy)
        if speed > max_speed:
            vx = (vx / speed) * max_speed
            vy = (vy / speed) * max_speed

        if distance <= speed:  # If close enough to waypoint, slow down
            if speed > 0:
                speed -= 1

            movement["target_index"] += 1

            # If at the end of the path, find new goal
            if movement["target_index"] >= len(path):
                movement["path"] = None
                movement["goal"] = None
                movement["needs_path"] = True

    def separate_enemies(self, enemy, enemies):
        total_x = 0
        total_y = 0
        count = 0

        for other in enemies:
            if other == enemy:  # ignore itself
                continue

            if other.need["type"] != "enemy":
                continue

            dist_sq = get_dist_sq(other.position, enemy.position)

            # if overlapping completely
            if dist_sq == 0:
                continue

            # get true distance
            other_pos = other.position
            enemy_pos = enemy.position

            # make push stronger if closer together
            if circle_collision(
                other_pos,
                other.collision_component["collider"],
                enemy_pos,
                enemy.collision_component["collider"],
            ):
                # account for new entity colliding
                count += 1

                sep_x, sep_y = circle_overlap_vector(
                    other_pos,
                    other.collision_component["collider"],
                    enemy_pos,
                    enemy.collision_component["collider"],
                )

                other.position[0] += sep_x
                other.position[1] += sep_y

                # Accumulate total force - (DONT FORGET TO DO THIS NEXT TIME!)
                total_x += sep_x
                total_y += sep_y

            if (
                count > 0
            ):  # get the average force over all entities applying force to this one
                total_x /= count
                total_y /= count

        return total_x, total_y

    def get_knockback(self):
        pass

    def get_collisions(self, enemy, entities):
        total_x = 0
        total_y = 0

        for other in entities:
            if other is enemy:  # Ignore Self
                continue

            if (
                other.need["type"] == "enemy" or other.need["type"] == "projectile"
            ):  # Ignore enemies and projectiles
                continue

            other_pos = other.position
            enemy_pos = enemy.position
            if circle_collision(
                enemy_pos,
                enemy.collision_component["collider"],
                other_pos,
                other.collision_component["collider"],
            ):
                sep_x, sep_y = circle_overlap_vector(
                    enemy_pos,
                    enemy.collision_component["collider"],
                    other_pos,
                    other.collision_component["collider"],
                )  # Fixed strength to act like wall

                # accumulate force
                total_x += sep_x
                total_y += sep_y

        return total_x, total_y

    def update(self, entities, grid):
        self.grid = grid
        enemies = list(entities.values())
        for enemy in enemies:
            movement = getattr(
                enemy, "movement_component", None
            )  # get the targets movement component

            if not movement:
                continue

            if not movement["path"] or movement["path"] is None:
                continue

            if movement["path_dirty"]:
                continue

            sep_force = self.separate_enemies(enemy, enemies)

            collision_force = self.get_collisions(enemy, enemies)

            self.move_towards_target(enemy, movement, sep_force, 0, collision_force)

            self.update_entity_grid_pos(grid, enemy)
