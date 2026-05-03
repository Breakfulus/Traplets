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

ATTACKS = {
    'single_shot': single_shot,
}