import pygame
import utils.consts as c

ENEMY_DEFINITIONS = {
    'mushant': {
        'need': {
            'catagory': c.ENEMIES
        },
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
            'goal': None,
            'prefered_target': 'base'
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
        'need': {
            'type': 'tower',
            'catagory': c.STRUCTURES
        },
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
            'image path': "yellow_cube.png",
            'image': None,
            'image_rect': None
        },
        "structure_component":{
            'footprint': [[1]],
            'selectable': True,
            'selected': False
        }
    },
        'base': {
        'need': {
            'type': 'base',
            'catagory': c.STRUCTURES
        },
        'health_component': {
            'max_health': 200,
            'health': 200
        },
        "rendering_component":{
            'image path': "purple_cube.png",
            'image': None,
            'image_rect': None
        },
        "structure_component":{
            'footprint': [[1]],
            'selectable': True,
            'selected': False
        }
    },
}