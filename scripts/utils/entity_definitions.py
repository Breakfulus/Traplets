import pygame
import utils.consts as c

ENEMY_DEFINITIONS = {
    'mushant': {
        'need': {
            'type': 'enemy',
            'layer': c.ENEMIES
        },
        'health_component': {
            'max_health': 200,
            'health': 200
        },
        'combat_component': {
            'type': 'single_shot',
            'range': 4,
            'cooldown': 2,
            'damage': 5,
            'targets': [],
            'target_priority': 'first'
        },
        'movement_component': {
            'speed': 3,
            'path': [],
            'target_index': 0,
            'needs_path': True,
            'path_dirty': False,
            'goal': None,
            'prefered_target': 'tower'
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
            'layer': c.STRUCTURES
        },
        'health_component': {
            'max_health': 200,
            'health': 200
        },
        'combat_component': {
            'type': 'single_shot',
            'range': 4,
            'cooldown': 2,
            'damage': 5,
            'targets': [],
            'target_priority': 'first',
            'last_shot': 0
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
            'layer': c.STRUCTURES
        },
        'health_component': {
            'max_health': 200,
            'health': 200
        },
        'combat_component': {
            'range': 0,
            'cooldown': 0,
            'damage': 0
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

PROJECTILE_DEFINITIONS = {
    'basic': {
        'need': {
            'type': 'projectile',
            'layer': c.PROJECTILES
        },

        "rendering_component":{
            'image path': "placeholder_player_projectile.png",
            'image': None,
            'image_rect': None
        }
    },
}