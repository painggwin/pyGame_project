import pygame.sprite
import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,playerSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png")
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * 0.5), int(self.size[1] * 0.5)))
        self.venom_image = pygame.image.load("venom player.png")
        venom_size = self.venom_image.get_size()
        self.venom_image = pygame.transform.scale(self.venom_image,(int(venom_size[0] * 0.4), int(venom_size[1] * 0.4)))
        self.flash_timer = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.playerSpeed = playerSpeed
        self.original_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.maxHealth = 5
        self.currentHealth = self.maxHealth
        self.info = pygame.display.Info()
        self.screenWidth = self.info.current_w
        self.screenHeight = self.info.current_h
        self.damage = 1
        self.venomTicks = 0
        self.venomDamage = 0
    def move (self,keys):
        # Initialize the movement vector
        move_x = 0
        move_y = 0
        # print(f"x: {self.rect.x} y: {self.rect.y}")

        # Check for key presses and update movement values
        if keys[pygame.K_a] and not self.rect.x < 5:
            move_x -= self.playerSpeed
        if keys[pygame.K_d] and not self.rect.x > self.screenWidth - 40:
            move_x += self.playerSpeed
        if keys[pygame.K_w] and not self.rect.y < 5:
            move_y -= self.playerSpeed
        if keys[pygame.K_s] and not self.rect.y > self.screenHeight - 40:
            move_y += self.playerSpeed

        if move_x != 0 and move_y != 0:
            magnitude = math.sqrt(move_x ** 2 + move_y ** 2)
            move_x /= magnitude
            move_y /= magnitude
            move_x *= self.playerSpeed
            move_y *= self.playerSpeed



        # Apply movement
        self.rect.x += move_x
        self.rect.y += move_y

        if move_x != 0 or move_y != 0:
            self.angle = math.degrees(math.atan2(move_y, move_x))
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def hit(self,enemy):
        dx = self.rect.x - enemy.rect.center[0]
        dy = self.rect.y - enemy.rect.center[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        repulsion_force = 5 / distance
        move_x = dx * repulsion_force
        move_y = dy * repulsion_force
        self.rect.x += move_x
        self.rect.y += move_y
    def venom(self):
        if self.venomTicks != 0:
            if self.venomTicks % 60 == 0:
                self.currentHealth -= math.ceil(self.venomDamage)
                self.flash_timer = 15
            self.venomTicks -= 1
        else:
            self.venomDamage = 0
        if self.flash_timer > 0:
            self.flash_timer -= 1
            rotated_image = pygame.transform.rotate(self.venom_image, -self.angle)
            self.image = rotated_image
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
            self.image = rotated_image
            self.rect = self.image.get_rect(center=self.rect.center)


