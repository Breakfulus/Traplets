import pygame

ENEMY_DEFINITIONS = {
    'mushant': {
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
            'speed': 0.25,
        },
        "rendering_component":{
            'image': "red_cube.png"
        }
    },
}

TOWER_DEFINITIONS = {
    'mushant': {
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
            'image': None
        }
    },
}