import pygame
import utils.consts as c

ENEMY_DEFINITIONS = {
    'template': {
        'need': {
            'type': 'enemy',
            'layer': c.ENEMIES,
            'target_layer': c.STRUCTURES
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
        'movement_component': {
            'speed': 3,
            'path': [],
            'target_index': 0,
            'needs_path': True,
            'path_dirty': False,
            'goal': None,
            'prefered_targets': ['base', 'tower', 'wall'],
            'final_tile': None
        },
        "collision_component":{
            'collider': 200,
            'is_colliding': False,
            'type': "enemy"
        },
        "rendering_component":{
            'image path': "red_cube.png",
            'image': None,
            'image_rect': None
        }
    },
}

TOWER_DEFINITIONS = {
    'template': {
        'need': {
            'type': 'tower',
            'layer': c.STRUCTURES,
            'target_layer': c.ENEMIES
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
        "collision_component":{
            'collider': 37,
            'is_colliding': False,
            'type': "structure"
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
            'layer': c.STRUCTURES,
            'target_layer': c.ENEMIES
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
        "collision_component":{
            'collider': 37,
            'is_colliding': False,
            'type': "structure"
        },
        "structure_component":{
            'footprint': [[1]],
            'selectable': True,
            'selected': False
        }
    },
}

PROJECTILE_DEFINITIONS = {
    'template': {
        'need': {
            'type': 'projectile',
            'layer': c.PROJECTILES
        },

        "rendering_component":{
            'image path': "placeholder_player_projectile.png",
            'image': None,
            'image_rect': None
        },

        "collision_component":{
            'collider': 18,
            'is_colliding': False,
            'type': "projectile"
        },

        "velocity_component": {
            'speed': 3,
            'velocity': [0, 0]
        }
    },
}