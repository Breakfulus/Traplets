import pygame
import utils.consts as c

class Tower(pygame.sprite.Sprite):
    footprint = [
            [1]
        ]

    def __init__(self, x, y, size=c.TILE_SIZE, tower_type='basic', attack_style='ranged'):
        pygame.sprite.Sprite.__init__(self)
        
        self.x = x
        self.y = y
        self.pos = self.x, self.y
        self.selected = False
        self.tower_type = tower_type
        self.range = size * 2
        self.image = pygame.Surface((size, size))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def draw_range(self, surf):
        if self.selected:
            pygame.draw.circle(surf, "blue", (self.rect.centerx, self.rect.centery), self.range, 5)

        

