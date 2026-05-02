import pygame

def get_dist_sq(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx*dx + dy*dy

def circle_collision(pos1, r1, pos2, r2):
    dist_sq = get_dist_sq(pos1, pos2)
    r = r1+r2

    return dist_sq <= r*r

def circle_overlap_vector(pos1, r1, pos2, r2):

    dist_sq = get_dist_sq(pos1, pos2)
    r = r1+r2

    #if objects are fully overlapping or completely out of the circle, dont return a force
    if dist_sq == 0 or dist_sq >= r:
        return (0, 0)
    
    #real distance
    dist = dist_sq ** 0.5
    #How much are they overlapping
    overlap = r-dist

    #normalize the vector
    dx /= dist
    dy /= dist

    #Returns vector direction scaled by overlap (Basically closer = stronger force)!
    return dx * overlap, dy * overlap