
import pygame.sprite
import pygame
import math

class enemyProjectile(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,speed,damage):
        super().__init__()

        self.image = pygame.image.load("ememy projectile.png")
        self.size = self.image.get_size()
        # self.image = pygame.transform.scale(self.image, (int(self.size[0] * 0.2), int(self.size[1] * 0.2)))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = [x, y]
        self.original_image = self.image
        self.angle = angle
        self.isExplosion = False
        self.isHeal = False
        self.damage = damage
        self.isVenom = False
        self.isLaser = False
    def move(self):
        self.image = pygame.transform.rotate(self.original_image, -self.angle + 180)
        self.rect = self.image.get_rect(center=self.rect.center)
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        self.rect.x += dx
        self.rect.y += dy
class healerProjectile(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,speed,heal,parent):
        pygame.sprite.Sprite.__init__(self)
        self.color = (247, 239, 82)
        self.size = (30, 30)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = [x, y]
        self.original_image = self.image
        self.angle = angle
        self.isExplosion = False
        self.isHeal = True
        self.heal = heal
        self.isVenom = False
        self.isLaser = False
        self.parent = parent
    def move(self):
        self.image = pygame.transform.rotate(self.original_image, - self.angle + 180)
        self.rect = self.image.get_rect(center=self.rect.center)
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        self.rect.x += dx
        self.rect.y += dy
class venomProjectile(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,speed,damage):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.color = (162, 13, 255)
        self.size = (30, 30)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = [x, y]
        self.original_image = self.image
        self.angle = angle
        self.isExplosion = False
        self.isHeal = False
        self.damage = damage
        self.isVenom = True
        self.isLaser = False
    def move(self):
        self.image = pygame.transform.rotate(self.original_image, -self.angle + 180)
        self.rect = self.image.get_rect(center=self.rect.center)
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        self.rect.x += dx
        self.rect.y += dy
class machineProjectile(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,speed,damage):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.color = (135, 135, 135)
        self.size = (20, 20)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = [x, y]
        self.original_image = self.image
        self.angle = angle
        self.isExplosion = False
        self.isHeal = False
        self.damage = damage
        self.isVenom = False
        self.isLaser = False
    def move(self):
        self.image = pygame.transform.rotate(self.original_image, -self.angle + 180)
        self.rect = self.image.get_rect(center=self.rect.center)
        dx = math.cos(math.radians(self.angle)) * self.speed
        dy = math.sin(math.radians(self.angle)) * self.speed
        self.rect.x += dx
        self.rect.y += dy


class Laser(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, damage, duration=60):
        pygame.sprite.Sprite.__init__(self)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration  # total frames the laser should exist
        self.timer = duration  # countdown timer
        self.thickness = 20  # laser line thickness
        self.color = (255, 0, 0)  # red color for the laser
        self.isHeal = False
        self.damage = damage
        self.isVenom = False
        self.isLaser = True
        self.isExplosion = False
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        laser_surface = pygame.Surface((int(distance), self.thickness), pygame.SRCALPHA)
        pygame.draw.line(laser_surface, self.color,(0, self.thickness // 2),(int(distance), self.thickness // 2),self.thickness)
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(laser_surface, angle)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=((self.start_pos[0] + self.end_pos[0]) / 2,(self.start_pos[1] + self.end_pos[1]) / 2))
