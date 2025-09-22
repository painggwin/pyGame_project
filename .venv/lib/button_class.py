import pygame
from pygame.locals import *

class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,connectedButton):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("button.png")
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * 0.3), int(self.size[1] * 0.3)))
        self.rect = self.image.get_rect()
        self.size = list(self.image.get_size())
        self.size[0] -= 12
        self.size[1] -= 12
        self.rect.center = [x,y]
        self.original_image = self.image
        self.lastButton = connectedButton
        self.visible = False

    def clickCheck(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.x + 10 <= mouse[0] <= self.rect.x + self.size[0] and self.rect.y + 10 <= mouse[1] <= self.rect.y + self.size[1]:
            print("hi")
            return True
        return False