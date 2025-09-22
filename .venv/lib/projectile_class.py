import pygame.sprite
import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,speed):
        super().__init__()
        self.image = pygame.image.load("projectile.png")
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * 0.2), int(self.size[1] * 0.2)))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = [x, y]
        self.original_image = self.image
        self.angle = angle
        self.isExplosion = False
        self.isHeal = False
        self.isVenom = False
    def move(self):
        self.image = pygame.transform.rotate(self.original_image, -self.angle + 180)
        self.rect = self.image.get_rect(center=self.rect.center)
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        self.rect.x += dx
        self.rect.y += dy
