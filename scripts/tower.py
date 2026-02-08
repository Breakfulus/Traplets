import pygame

class Tower:
    def __init__(self, x, y, size, tower_type='basic', attack_style='ranged'):
        self.x = x
        self.y = y
        self.pos = self.x, self.y
        self.selected = False
        self.tower_type = tower_type
        self.range = size * 2
        self.rect = pygame.Rect(x - size/4, y - size/4, size/2, size/2)
    
    def draw(self, screen):
        pygame.draw.rect(screen, 'white', self.rect)

        if self.selected:
            pygame.draw.circle(screen, "blue", (self.x, self.y), self.range, 5)

