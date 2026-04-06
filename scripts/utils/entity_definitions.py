import pygame
import utils.consts as c

ENEMY_DEFINITIONS = {
    'mushant': {
        'need': {'type': c.ENEMIES},
        'health_component': {
            'max_health': 200,
            'health': 200
        },
        'combat_component': {
            'range': 2,
            'attack_speed': 2,
            'damage': 5
        },
        'movement_component': {
            'speed': 3,
            'path': [],
            'target_index': 0,
            'needs_path': True,
            'goal': None
        },
        "rendering_component":{
            'image path': "red_cube.png",
            'image': None,
            'image_rect': None
        }
    },
}

TOWER_DEFINITIONS = {
    'mushant': {
        'need': {'type': c.STRUCTURES},
        'health_component': {
            'max_health': 200,
            'health': 200
        },
        'combat_component': {
            'range': 2,
            'attack_speed': 2,
            'damage': 5
        },
        "rendering_component":{
            'image path': "red_cube.png",
            'image': None,
            'image_rect': None
        },
        "structure_component":{
            'footprint': [[1, 1]],
            'selectable': True,
            'selected': False
        }
    },
}