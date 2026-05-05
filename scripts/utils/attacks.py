import pygame
import math
from utils.entity_definitions import *

def single_shot(attacker, target, spawn_projectile):
    dx = target.position[0] - attacker.position[0]
    dy = target.position[1] - attacker.position[1]

    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    
    dx /= dist
    dy /= dist

    projectile = spawn_projectile
    speed = projectile.velocity_component['speed']

    projectile.velocity_component["velocity"] = [dx * speed, dy * speed]
    projectile.damage_component['damage'] = attacker.combat_component['damage']
    print(f"TEAM: {projectile.team}")

def area_of_effect(attacker, target, conditional):
    for entity in attacker.combat_component["targets"]:
        if entity.need["type"] != "projectile":
            print(f"TARGET HEALTH: {target.health_component['health']}")
            entity.health_component['health'] -= attacker.combat_component['damage']

ATTACKS = {
    'single_shot': single_shot,
    'area_of_effect': area_of_effect
}