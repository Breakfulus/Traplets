import pygame
import math
import random

def get_dist_sq(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx*dx + dy*dy

def circle_collision(pos1, r1, pos2, r2):
    dist_sq = get_dist_sq(pos1, pos2)
    r = r1+r2

    return dist_sq <= r*r

def circle_overlap_vector(pos1, r1, pos2, r2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    force_x = 0
    force_y = 0

    dist_sq = get_dist_sq(pos1, pos2)
    r = r1+r2

    #if objects are fully overlapping or completely out of the circle, dont return a force
    if dist_sq == 0:
        angle = random.uniform(0, 2 * math.pi)
        return math.cos(angle) * .5, math.sin(angle) * .5
    
    #real distance
    dist = math.sqrt(dist_sq)

    if dist <= r:
        #How much are they overlapping
        overlap =  r - dist

        #normalize the vector
        dx /= dist
        dy /= dist
    
        strength = .5

        overlap_ratio = overlap / r
        force = overlap_ratio ** 2 #quadratic falloff

        if overlap_ratio > 0.6:
            force *= 2

        #Scales normalized vector by overlap (Basically closer = stronger force)!
        force_x = dx * force * strength * r
        force_y = dy * force * strength *r

        max_force = 8 #cap force by this number

        #grab the length of vector/magnitude
        mag = math.sqrt(force_x ** 2 + force_y ** 2)

        if mag > max_force: #If force is too strong, normalize forces and then scale to max force
            force_x = (force_x / mag) * max_force
            force_y = (force_y / mag) * max_force
    
    return force_x, force_y

