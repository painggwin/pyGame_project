import math
import time
from base64 import b32decode
import pygame
from pygame.locals import *
import player_class
import enemies_class
import projectile_class
import random
import data_class
import button_class
import boss_class
pygame.init()

clock = pygame.time.Clock()
data = data_class.Data()
screen = pygame.display.set_mode((data.screenWidth,data.screenHeight),pygame.RESIZABLE)
pygame.display.set_caption("Game Name")

gameSprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemyProjectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
upgradeButtons = pygame.sprite.Group()
lines = []
def spawnEnemy():
    if not data.bossAlive:
        if random.random() < 0.5:
            enemyX = random.choice([-50, data.screenWidth + 50])
            enemyY = random.randint(50, data.screenHeight - 50)
        else:
            enemyX = random.randint(50, data.screenWidth - 50)
            enemyY = random.choice([-50, data.screenHeight + 50])
        randomMultipier = random.randint(2,3) / 2
        enemyHealth = (math.ceil(3.042228491 * (1.1109767275 ** data.currentRound)) - 3) * randomMultipier

        enemyDict = enemies_class.getEnemy(enemyX,enemyY,randomMultipier,enemyHealth,data.enemySpeed)
        availableCount = min((data.currentRound // 10) + 1, len(enemyDict))
        availableEnemies =  list(enemyDict.values())[:availableCount]
        weights = [9] + [5] * (availableCount - 1)
        enemy = random.choices(availableEnemies, weights=weights, k=1)[0]

        enemies.add(enemy)
        gameSprites.add(enemy)
def boss():
    data.enemyX = random.randint(-30, data.screenWidth + 30)
    data.enemyY = random.randint(30, data.screenHeight - 30) if data.enemyX < 0 or data.enemyX > data.screenWidth + 30 else random.choice([-30, data.screenHeight + 30])
    enemy = boss_class.boss(data.enemyX, data.enemyY, data.enemySpeed,(math.ceil(3.042228491 * (1.1109767275 ** data.currentRound)) - 3) * 10)
    enemies.add(enemy)
    gameSprites.add(enemy)
    data.bossAlive = True
def drawLines():
    for line in lines:
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 3)
def shoot(x,y,angle):
    projectile = projectile_class.Projectile(x,y,angle,20)
    projectiles.add(projectile)
    gameSprites.add(projectile)
def bar(sprite):
    if sprite.currentHealth == 0:
        healthPercentage = -10
    else:
        healthPercentage = sprite.currentHealth/sprite.maxHealth
    currentBarWidth = data.barWidth * healthPercentage
    multplier = 1
    if sprite in enemies.sprites():
        multplier = sprite.sizeMultipier
    pygame.draw.rect(screen, (0, 255, 0), (sprite.rect.x - 8, sprite.rect.y - data.barHeight - 10, data.barWidth * multplier + 13 , data.barHeight + 8))
    pygame.draw.rect(screen, (0, 0, 0), (sprite.rect.x, sprite.rect.y - data.barHeight - 8, data.barWidth * multplier, data.barHeight+3))
    pygame.draw.rect(screen, (0, 255, 0), (sprite.rect.x, sprite.rect.y - data.barHeight - 8, currentBarWidth * multplier, data.barHeight+3))
def pause():
    while True:
        clock.tick(data.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
def drawRound():
    font = pygame.font.Font(None, 30)
    text = font.render(f"Round: {data.currentRound}", True, (255,255,255))
    textRect = text.get_rect(center=(50, 20))
    screen.blit(text, textRect)

    font = pygame.font.Font(None, 30)
    text = font.render(f"kills: {data.kills}", True, (255,255,255))
    textRect = text.get_rect(center=(data.screenWidth-50, 20))
    screen.blit(text, textRect)
class BranchTree:
    def __init__(self):
        self.startX =  data.screenWidth / 2
        self.startY =  data.screenHeight / 2
        self.spacingX = 100
        self.spacingY = 100
        self.levels = []

    def addButton(self, branchIndex):
        currentLevel = branchIndex[0]
        if currentLevel >= len(self.levels):
            self.levels.append([])

        ring = math.ceil(currentLevel / 4)

        indexInLevel = len(self.levels[currentLevel])

        direction = currentLevel % 4

        radius = int(ring * 150)
        x, y = self.startX, self.startY


        if direction == 0:  # Right
            x = self.startX + radius
            if ring % 2 == 0:
                y = self.startY - ((indexInLevel - 1) * self.spacingY) / 2
            else:
                y = self.startY + ((indexInLevel - 1) * self.spacingY) / 2
        elif direction == 1:  # Down
            y = self.startY + radius
            if ring % 2 == 0:
                x = self.startX - ((indexInLevel - 1) * self.spacingX) / 2
            else:
                x = self.startX + ((indexInLevel - 1) * self.spacingX) / 2

        elif direction == 2:  # Left
            x = self.startX - radius
            if ring % 2 == 0:
                y = self.startY - ((indexInLevel - 1) * self.spacingY) / 2
            else:
                y = self.startY + ((indexInLevel - 1) * self.spacingY) / 2

        elif  direction == 3: # Up
            y = self.startY - radius
            if ring % 2 == 0:
                x = self.startX - ((indexInLevel - 1) * self.spacingX) / 2
            else:
                x = self.startX + ((indexInLevel - 1) * self.spacingX) / 2
        if currentLevel == 0:
            x, y = self.startX, self.startY

        # print(currentLevel, " ", direction, " ", ring, " ", radius, " ", y)
        if currentLevel > 0:
            button = button_class.Button(x, y, self.levels[max(0,currentLevel - 4)][branchIndex[1] - 1])
            button.image.set_alpha(0)
        else:
            button = button_class.Button(x, y, None)
            button.visible = True
        upgradeButtons.add(button)
        self.levels[currentLevel].append(button)

        # if currentLevel == 4:
        #     print(button.rect.center)

    def buttonClicked(self,button):
        for level in range(len(self.levels)):
            for currentButton in self.levels[level]:
                if currentButton.lastButton is not None:
                    if currentButton.lastButton == button:
                        currentButton.visible = True
                        currentButton.image.set_alpha(255)
                        lines.append((currentButton.rect.center, button.rect.center))

def game():
    """
    Main game loop.
    Initializes the player, handles events, updates sprites and collisions,
    manages rounds, and updates the UI.
    """
    # Clear any existing enemy projectiles.
    enemyProjectiles.empty()

    # Initialize the player at the center of the screen.
    player = player_class.Player(
        int(data.screenWidth / 2),
        int(data.screenHeight / 2),
        data.playerSpeed
    )
    gameSprites.add(player)

    while True:
        # Cap the frame rate and get the elapsed time.
        delta_time = clock.tick(data.fps)
        data.tickCount += 1

        # Process events (e.g. quit event).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Clear the screen with a background color.
        screen.fill((47, 40, 39))

        # Decrease invulnerability frames and attack cooldown if active.
        if data.iFrames > 0:
            data.iFrames -= 1
        if data.attackCooldown > 0:
            data.attackCooldown -= 1

        # ----- Round and Level Management -----
        # data.killsNeeded = 1
        if data.killsThisRound >= int(data.killsNeeded) or data.bossKilled:
            if data.currentRound < 100:
                data.currentRound += 1
                data.killsThisRound = 0
                data.killsNeeded *= 1.05
                data.enemySpawnTime = int(0.9755 ** data.currentRound * data.enemySpawnTime + 10)

                # Remove all existing enemies and enemy projectiles.
                for enemy in enemies:
                    enemy.kill()
                for projectile in enemyProjectiles:
                    projectile.kill()

                # Spawn a boss every 10 rounds.
                if data.currentRound % 10 == 0:
                    boss()
                data.bossKilled = False

        # ----- Player Input and Shooting -----
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and data.attackCooldown == 0:
            shoot(player.rect.center[0], player.rect.center[1], player.angle)
            data.attackCooldown += data.attackSpeed

        # Check collisions between the player and enemies.
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)
        if collided_enemies:
            enemy_hit = collided_enemies[0]
            player.hit(enemy_hit)
            if data.iFrames == 0:
                player.currentHealth = int(player.currentHealth - enemy_hit.damage)
                data.iFrames += 30

        # End game if the player is dead.
        if player.currentHealth <= 0:
            bar(player)
            gameSprites.draw(screen)
            pygame.display.update()
            break

        # ----- Player Movement -----
        player.move(pygame.key.get_pressed())

        # ----- Enemy Spawning -----
        # Spawn a wave if there are no enemies (except possibly at round start).
        if len(enemies.sprites()) == 0 and (data.killsThisRound != 0 or data.currentRound == 1):
            spawn_amount = (5 + math.floor(data.currentRound * 1.5)
                            if data.currentRound < 15 else 30)
            for _ in range(spawn_amount):
                spawnEnemy()
        # Spawn an enemy periodically based on tick count.
        if data.tickCount % data.enemySpawnTime == 0:
            spawnEnemy()

        # ----- Enemy Behavior and Shooting -----
        for enemy in enemies:
            # Move enemy based on type.
            if enemy.__class__.__name__ != "healerEnemy":
                enemy.move(player.rect.x, player.rect.y, enemies)
            else:
                enemy.move(enemies, player)

            # If the enemy can shoot, process its attack.
            if enemy.isShooter:
                if enemy.attackCooldown > 0:
                    enemy.attackCooldown -= 1

                # Healer enemies shoot differently.
                if enemy.__class__.__name__ != "healerEnemy":
                    projectile = enemy.shoot(player.rect.x, player.rect.y, enemy.damage)
                else:
                    projectile = enemy.shoot()
                    if projectile is not None:
                        projectiles.add(projectile)
                if projectile is not None:
                    enemyProjectiles.add(projectile)
                    gameSprites.add(projectile)

            # For orange enemies, handle explosion animation and spawn an explosion projectile.
            if enemy.__class__.__name__ == "orangeEnemy" and enemy.exploded:
                if enemy.animateExplosion(delta_time):
                    explosion = enemies_class.explosion(
                        enemy.rect.center[0],
                        enemy.rect.center[1],
                        enemy.damage
                    )
                    projectiles.add(explosion)
                    enemyProjectiles.add(explosion)
                    gameSprites.add(explosion)

            # For laser enemies, draw a laser line when in a specific attack cooldown range.
            if enemy.__class__.__name__ == "laserEnemy" and (enemy.attackCooldown > 130 and enemy.attackCooldown > 60):
                pygame.draw.line(screen, (255, 0, 0), enemy.rect.center, enemy.end_pos, width=5)

        # ----- Enemy Projectile Handling -----
        for projectile in enemyProjectiles:
            # For non-explosion and non-laser projectiles, move them and kill if off screen.
            if not projectile.isExplosion and not projectile.isLaser:
                projectile.move()
                if (projectile.rect.x > data.screenWidth or projectile.rect.x < 0 or
                        projectile.rect.y > data.screenHeight or projectile.rect.y < 0):
                    projectile.kill()

            # Check collision between enemy projectiles and the player.
            if not projectile.isLaser:
                if pygame.sprite.collide_rect(player, projectile):
                    if projectile.isExplosion:
                        if projectile.dead != 0:
                            if data.iFrames == 0:
                                player.currentHealth -= projectile.damage
                                data.iFrames += 30
                            projectile.dead = 1
                    elif projectile.isHeal:
                        if data.iFrames == 0:
                            player.currentHealth -= math.ceil(projectile.heal)
                            data.iFrames += 30
                        projectile.kill()
                    elif projectile.isVenom:
                        player.venomTicks = 240
                        player.venomDamage = projectile.damage
                        projectile.kill()
                    else:
                        if data.iFrames == 0:
                            player.currentHealth = int(player.currentHealth - projectile.damage)
                            data.iFrames += 30
                        projectile.kill()
            else:
                # For laser projectiles, use mask-based collision detection.
                if pygame.sprite.collide_mask(player, projectile):
                    if data.iFrames == 0:
                        player.currentHealth = int(player.currentHealth - projectile.damage)
                        data.iFrames += 30

        # Apply any ongoing venom effects to the player.
        player.venom()

        # ----- Draw Health Bars -----
        for enemy in enemies:
            bar(enemy)
        bar(player)

        # ----- Player Projectile Handling -----
        for projectile in projectiles:
            if projectile.isExplosion:
                projectile.timer -= 1
                if projectile.timer <= 0:
                    projectile.kill()
            else:
                projectile.move()

            # Kill the projectile if it goes off screen (non-explosions).
            if (projectile.rect.x > data.screenWidth or projectile.rect.x < 0 or
                    projectile.rect.y > data.screenHeight or projectile.rect.y < 0):
                if not projectile.isExplosion:
                    projectile.kill()

            # Check collisions between projectiles and enemies.
            for enemy in enemies:
                if pygame.sprite.collide_rect(enemy, projectile):
                    if projectile.isExplosion:
                        if projectile.dead != 0:
                            enemy.currentHealth = int(enemy.currentHealth - projectile.damage)
                            projectile.dead = 1
                    elif projectile.isHeal:
                        # Prevent an enemy from healing itself.
                        if projectile.parent != enemy:
                            enemy.currentHealth += math.ceil(projectile.heal)
                            enemy.currentHealth = min(enemy.currentHealth, enemy.maxHealth)
                            projectile.kill()
                    else:
                        projectile.kill()
                        enemy.currentHealth = int(enemy.currentHealth - player.damage)

                    # Remove the enemy if its health is depleted.
                    if enemy.currentHealth <= 0:
                        enemy.kill()
                        data.kills += 1
                        data.killsThisRound += 1
                        if enemy.__class__.__name__ == "boss":
                            data.bossAlive = False
                            data.bossKilled = True

            # Reset explosion projectile state if necessary.
            if projectile.isExplosion and projectile.dead == 1:
                projectile.dead = 0

        # ----- UI Rendering -----
        font = pygame.font.Font(None, 30)
        health_text = font.render(
            f"health: {player.currentHealth}/{player.maxHealth}", True, (255, 255, 255)
        )
        text_rect = health_text.get_rect(center=(data.screenWidth - 50, 50))
        screen.blit(health_text, text_rect)

        # Draw all sprites and round/kill progress indicators.
        gameSprites.draw(screen)
        drawRound()
        pygame.draw.rect(screen, (0, 0, 0), (5, 33, 85, 15))
        progress_width = 85 * (data.killsThisRound / data.killsNeeded)
        pygame.draw.rect(screen, (0, 255, 0), (5, 33, progress_width, 15))
        pygame.display.update()

    # Clean up sprites after game over.
    gameSprites.empty()
    projectiles.empty()
    enemies.empty()
def upgradeMenu():
    tree = BranchTree()
    buttonsAdded = False
    debug = 0
    while True:
        clock.tick(data.fps)
        debug += 1
        if data.buttonDelay != 0:
            data.buttonDelay -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if data.buttonDelay == 0:
                    for button in upgradeButtons:
                        if button.visible:
                        # pygame.draw.rect(screen,(0,0,0),(button.rect.x + 10,button.rect.y + 10, button.size[0], button.size[1]))
                        # pygame.display.update()
                            if button.clickCheck():
                                tree.buttonClicked(button)
                                data.buttonDelay = 5
                                break
        screen.fill((47, 40, 39))
        tree.addButton((0,0))
        if not buttonsAdded:
            for b in range(8):
                tree.addButton((b+1,0))
                tree.addButton((b+1,0))
                tree.addButton((b+1,1))
                buttonsAdded = True

        drawLines()
        upgradeButtons.draw(screen)
        pygame.display.update()
        # pause()
run = True


while run:
    # game()
    data = data_class.Data()
    upgradeMenu()
pygame.quit()