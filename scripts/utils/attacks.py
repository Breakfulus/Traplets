import pygame
import math
from utils.entity_definitions import *

''' This is a helper file. All the different type of attacks live here and can be called from the ATTACKS dict.
Provides context for the many different attack types without the need for nesting code and endless if chains.
To add an attack put its capabilities into its own method, attacks can be litterally about any action. 
If your attack needs context the generic context doesnt provide, simply add it to the generic context dict in the combat_system.py file.
'''

def single_shot(attacker, context):
    target = context["target"]
    manager = context["manager"]
    dx = target.position[0] - attacker.position[0]
    dy = target.position[1] - attacker.position[1]

    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    
    dx /= dist
    dy /= dist

    projectile = manager.create_entity(
                PROJECTILE_DEFINITIONS['template'],
                (attacker.position[0], attacker.position[1]),
                [(0, 0)],
                attacker.team,
                eid=None
            )
    speed = projectile.velocity_component['speed']

    projectile.velocity_component["velocity"] = [dx * speed, dy * speed]
    projectile.damage_component['damage'] = attacker.combat_component['damage'] #Give damage stat from attacker to projectile
    print(f"TEAM: {projectile.team}")

def area_of_effect(attacker, context):
    apply_damage = context["apply_damage"]

    for entity in attacker.combat_component["targets"]:

        #Apply damage to all targets in range
        apply_damage(attacker.combat_component["damage"], entity)
            

ATTACKS = {
    'single_shot': single_shot,
    'area_of_effect': area_of_effect,
}