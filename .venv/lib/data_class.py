import pygame
from sympy import false


class Data:
    def __init__(self):
        self.fps = 60
        self.playerSpeed = 5
        self.info = pygame.display.Info()
        self.screenWidth = self.info.current_w
        self.screenHeight = self.info.current_h
        self.enemySpeed = 2
        self.tickCount = 0
        self.enemySpawnTime = 120
        self.iFrames = 0
        self.attackCooldown = 0
        self.attackSpeed = 20
        self.barWidth = 70
        self.barHeight = 5
        self.buttonDelay = 0
        self.currentRound = 1
        self.kills = 0
        self.killsNeeded = 15
        self.killsThisRound = 0
        self.bossAlive = False
        self.bossKilled = False