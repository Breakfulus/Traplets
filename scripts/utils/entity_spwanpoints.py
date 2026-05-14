import random
import utils.consts as c

def get_possible_spawn_points():
    rows = c.GRID_HEIGHT - 1
    cols = c.GRID_WIDTH - 1
    points = []

    for ri in range(rows):
        point = (0, ri)
        points.append(point)

        for ci in range(cols):
            point = (ci, 0)
            points.append(point)
    return set(points)

def get_next_spawn_point():
    next_spawn = random.choice(list(c.SPAWN_POINTS))
    return next_spawn
