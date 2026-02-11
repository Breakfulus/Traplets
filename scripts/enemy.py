import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, rect_size, waypoints, damage, speed, range, health, image):
        pygame.sprite.Sprite.__init__(self)
        #the later stuff
        self.damage = damage
        self.health = health
        self.range = range
        self.speed = speed
        #Sprites big stuff
        self.waypoints = waypoints
        self.target = 0
        self.x = x
        self.y = y
        self.image = pygame.Surface((rect_size, rect_size))
        self.image.fill('red')
        self.rect = pygame.Rect(self.x, self.y, rect_size, rect_size)
    
    def move_toward_point(self):
        target_waypoint = self.waypoints[self.target]
        dx = target_waypoint[0] - self.x
        dy = target_waypoint[1] - self.y

        distance = (dx**2 + dy**2) ** .5

        if distance <= self.speed:
            self.x, self.y = target_waypoint
            self.target += 1
            if self.target >= len(self.waypoints):
                self.target = 0
            return
        
        if dx != 0:
            self.x += self.speed if dx > 0 else -self.speed
        elif dy != 0:
            self.y += self.speed if dy > 0 else -self.speed


    def take_damage(self, damage_taken):
        self.health -= damage_taken
    
    def update(self):
        if self.waypoints:
            self.move_toward_point()
        else:
            return
        self.rect.center = self.x, self.y
    
    def draw(self, surf):
        surf.blit(self.image, self.rect)

