import pygame
import math
from utils.entity_definitions import *

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