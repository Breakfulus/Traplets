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
            'speed': 3,
            'path': [],
            'target_index': 0
        },
        "rendering_component":{
            'image path': "red_cube.png",
            'image': None
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
            'image path': "red_cube.png",
            'image': None
        },
        "placement_component":{
            'footprint': [[1]]
        }
    },
}