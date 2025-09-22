import pygame.sprite
import pygame
import math

class boss(pygame.sprite.Sprite):
    def __init__(self,x,y,enemySpeed,maxHealth):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = 3
        self.color = (255, 0, 0)
        self.size = (200, 200)  # Width and height of the circle
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, (0, 0, self.size[0], self.size[1]))  # Draw a square
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = enemySpeed
        self.original_image = self.image
        self.maxHealth = maxHealth
        self.currentHealth = self.maxHealth
        self.damage = self.maxHealth/5
    def move (self,playerX,playerY,enemies):
        move_x = 0
        move_y = 0


        if playerX < self.rect.x:
            move_x -= self.enemySpeed
        if playerX > self.rect.x:
            move_x += self.enemySpeed
        if playerY < self.rect.y:
            move_y -= self.enemySpeed
        if playerY > self.rect.y:
            move_y += self.enemySpeed

        if move_x != 0 and move_y != 0:
            magnitude = math.sqrt(move_x ** 2 + move_y ** 2)
            move_x /= magnitude
            move_y /= magnitude
            move_x *= self.enemySpeed
            move_y *= self.enemySpeed


        for enemy in enemies:
            if enemy == self:
                continue
            dx = self.rect.x - enemy.rect.center[0]
            dy = self.rect.y - enemy.rect.center[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance < 100:
                if distance > 0:
                    repulsion_force = 2 / distance
                    move_x += dx * repulsion_force
                    move_y += dy * repulsion_force

        self.rect.x += move_x
        self.rect.y += move_y