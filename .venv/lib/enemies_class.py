import pygame.sprite
import pygame
import math
import random
import ememy_projectile_class

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,enemySpeed,maxHealth,randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier
        self.color = (255, 0, 0)
        self.size = (55 * randomMultipier, 55 * randomMultipier)  # Width and height of the circle
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = enemySpeed
        self.original_image = self.image
        self.maxHealth = maxHealth
        # self.maxHealth = 1
        self.currentHealth = self.maxHealth
        self.damage = self.maxHealth/2
        self.isShooter = False
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


class greenEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemySpeed,maxHealth,randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier
        self.color = (98, 255, 0)
        self.size = (55 * randomMultipier, 55 * randomMultipier)  # Width and height of the circle
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = enemySpeed
        self.original_image = self.image
        self.maxHealth = maxHealth
        self.currentHealth = self.maxHealth
        self.attackSpeed = 300
        self.attackCooldown = self.attackSpeed
        self.info = pygame.display.Info()
        self.screenWidth = self.info.current_w
        self.screenHeight = self.info.current_h
        self.damage = self.maxHealth
        self.outerLimit = random.randint(300, 450)
        self.innerLimit = self.outerLimit - 100
        self.isShooter = True
    def shoot(self,playerX,playerY,damage):
        if self.attackCooldown == 0:
            dx = playerX - self.rect.center[0]
            dy = playerY - self.rect.center[1]
            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
            projectile = ememy_projectile_class.enemyProjectile(self.rect.center[0],self.rect.center[1],angle,3,damage)
            self.attackCooldown = self.attackSpeed
            return projectile

    def move(self,playerX,playerY,enemies):

        dx = playerX - self.rect.x
        dy = playerY - self.rect.y
        distance = math.hypot(dx, dy)

        if distance < self.innerLimit:
            direction = -1
        elif distance > self.outerLimit:
            direction = 1
        else:
            direction = 0


        move_x = direction * (self.enemySpeed if dx > 0 else -self.enemySpeed)
        move_y = direction * (self.enemySpeed if dy > 0 else -self.enemySpeed)

        if move_x != 0 and move_y != 0:
            length = math.hypot(move_x, move_y)
            move_x = (move_x / length) * self.enemySpeed
            move_y = (move_y / length) * self.enemySpeed

        for enemy in enemies:
            if enemy == self:
                continue
            dx = self.rect.x - enemy.rect.center[0]
            dy = self.rect.y - enemy.rect.center[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance < 100:
                if distance > 0:
                    repulsion_force = 1 / distance
                    move_x += dx * repulsion_force
                    move_y += dy * repulsion_force



        if self.rect.y > self.screenHeight - 40:
            move_y = -5
        if self.rect.x > self.screenWidth - 40:
            move_x = -5
        if self.rect.y < 5:
            move_y = 5
        if self.rect.x < 5:
            move_x = 5


        self.rect.x += move_x
        self.rect.y += move_y


class orangeEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y,enemySpeed,maxHealth,randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier
        self.color = (255, 136, 0)
        self.size = (55 * randomMultipier, 55 * randomMultipier)  # Width and height of the circle
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = enemySpeed
        self.original_image = self.image
        self.maxHealth = maxHealth
        self.currentHealth = self.maxHealth
        self.exploded = False
        self.flashTimer = 0
        self.flashInterval = 125
        self.isWhite = False
        self.explodeTicks = 0
        self.damage = self.maxHealth*2
        self.isShooter = False

    def animateExplosion(self, deltaTime):
        if self.exploded:
            self.flashTimer += deltaTime
            if self.flashTimer >= self.flashInterval:
                self.isWhite = not self.isWhite
                self.flashTimer = 0
                self.explodeTicks += 1
                if self.explodeTicks >= 5:
                    self.kill()
                    return True
            color = (255, 255, 255) if self.isWhite else (255, 136, 0)
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(self.image, color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        return False

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

        distance = math.sqrt((self.rect.center[0] - playerX) ** 2 + (self.rect.center[1] - playerY) ** 2)
        if distance <= 150 or self.exploded:
            move_x = 0
            move_y = 0
            self.exploded = True


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


class explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,damage):
        pygame.sprite.Sprite.__init__(self)
        self.color = (255, 255, 255)
        self.size = (300,300)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.timer = 10
        self.isExplosion = True
        self.isHeal = False
        self.isLaser = True
        self.isVenom = False
        self.dead = 2
        self.damage = damage


class healerEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemySpeed,maxHealth,randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier
        self.color = (255, 244, 25)
        self.size = (55 * randomMultipier, 55 * randomMultipier)  # Width and height of the circle
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = enemySpeed
        self.original_image = self.image
        self.maxHealth = maxHealth
        self.currentHealth = self.maxHealth
        self.attackSpeed = 180
        self.attackCooldown = self.attackSpeed
        self.info = pygame.display.Info()
        self.screenWidth = self.info.current_w
        self.screenHeight = self.info.current_h
        self.damage = self.maxHealth/4
        self.outerLimit = random.randint(300, 450)
        self.innerLimit = self.outerLimit - 30
        self.target = None
        self.isShooter = True

    def move(self,enemies,player):
        min_distance = 800
        closestEnemy = None
        for enemy in enemies:
            if enemy == self or enemy.rect.y > self.screenHeight - 40 or enemy.rect.x > self.screenWidth - 40 or enemy.rect.y < 5 or enemy.rect.x < 5 or enemy.currentHealth == enemy.maxHealth:
                continue
            dx = enemy.rect.center[0] - self.rect.center[0]
            dy = enemy.rect.center[1] - self.rect.center[1]
            distance = math.hypot(dx, dy)
            if distance < min_distance:
                min_distance = distance
                closestEnemy = enemy
        if closestEnemy is None:
            closestEnemy = player
        self.target = closestEnemy


        dx = self.target.rect.center[0] - self.rect.center[0]
        dy = self.target.rect.center[1] - self.rect.center[1]
        distance = math.hypot(dx, dy)

        if distance < self.innerLimit:
            direction = -1
        elif distance > self.outerLimit:
            direction = 1
        else:
            direction = 0


        move_x = direction * (self.enemySpeed if dx > 0 else -self.enemySpeed)
        move_y = direction * (self.enemySpeed if dy > 0 else -self.enemySpeed)

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
                    repulsion_force = 1 / distance
                    move_x += dx * repulsion_force
                    move_y += dy * repulsion_force



        if self.rect.y > self.screenHeight - 40:
            move_y = -5
        if self.rect.x > self.screenWidth - 40:
            move_x = -5
        if self.rect.y < 5:
            move_y = 5
        if self.rect.x < 5:
            move_x = 5


        self.rect.x += move_x
        self.rect.y += move_y

    def shoot(self):
        if self.attackCooldown == 0:
            dx = self.target.rect.center[0] - self.rect.center[0]
            dy = self.target.rect.center[1] - self.rect.center[1]
            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
            projectile = ememy_projectile_class.healerProjectile(self.rect.center[0],self.rect.center[1],angle,10,self.damage,self)
            self.attackCooldown = self.attackSpeed
            return projectile


class purpleEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemySpeed,maxHealth,randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier
        self.color = (162, 13, 255)
        self.size = (55 * randomMultipier, 55 * randomMultipier)  # Width and height of the circle
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = enemySpeed
        self.original_image = self.image
        self.maxHealth = maxHealth
        self.currentHealth = self.maxHealth
        self.attackSpeed = 180
        self.attackCooldown = self.attackSpeed
        self.info = pygame.display.Info()
        self.screenWidth = self.info.current_w
        self.screenHeight = self.info.current_h
        self.damage = self.maxHealth/4
        self.outerLimit = random.randint(300, 450)
        self.innerLimit = self.outerLimit - 100
        self.isShooter = True
    def shoot(self,playerX,playerY,damage):
        if self.attackCooldown == 0:
            dx = playerX - self.rect.center[0]
            dy = playerY - self.rect.center[1]
            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
            projectile = ememy_projectile_class.venomProjectile(self.rect.center[0],self.rect.center[1],angle,5,damage)
            self.attackCooldown = self.attackSpeed
            return projectile

    def move(self,playerX,playerY,enemies):

        dx = playerX - self.rect.x
        dy = playerY - self.rect.y
        distance = math.hypot(dx, dy)

        if distance < self.innerLimit:
            direction = -1
        elif distance > self.outerLimit:
            direction = 1
        else:
            direction = 0


        move_x = direction * (self.enemySpeed if dx > 0 else -self.enemySpeed)
        move_y = direction * (self.enemySpeed if dy > 0 else -self.enemySpeed)

        if move_x != 0 and move_y != 0:
            length = math.hypot(move_x, move_y)
            move_x = (move_x / length) * self.enemySpeed
            move_y = (move_y / length) * self.enemySpeed


        for enemy in enemies:
            if enemy == self:
                continue
            dx = self.rect.x - enemy.rect.center[0]
            dy = self.rect.y - enemy.rect.center[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance < 100:
                if distance > 0:
                    repulsion_force = 1 / distance
                    move_x += dx * repulsion_force
                    move_y += dy * repulsion_force



        if self.rect.y > self.screenHeight - 40:
            move_y = -5
        if self.rect.x > self.screenWidth - 40:
            move_x = -5
        if self.rect.y < 5:
            move_y = 5
        if self.rect.x < 5:
            move_x = 5


        self.rect.x += move_x
        self.rect.y += move_y


class enemyTank(pygame.sprite.Sprite):
    def __init__(self, x, y, enemySpeed, maxHealth, randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier
        self.color = (23, 194, 0)
        self.size = (100 * randomMultipier, 100 * randomMultipier)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        center = (self.size[0] // 2, self.size[1] // 2)
        radius = self.size[0] // 2
        points = []
        for i in range(5):
            angle = math.radians(-90 + i * (360 / 5))
            x_coord = center[0] + radius * math.cos(angle)
            y_coord = center[1] + radius * math.sin(angle)
            points.append((x_coord, y_coord))
        pygame.draw.polygon(self.image, self.color, points)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = math.ceil(enemySpeed/3)
        self.original_image = self.image
        self.maxHealth = maxHealth*5
        # self.maxHealth = 1
        self.currentHealth = self.maxHealth
        self.damage = self.maxHealth/5
        self.sizeMultipier = randomMultipier * 1.7
        self.isShooter = False
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


class fastEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y,enemySpeed,maxHealth,randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier/2
        self.color = (0, 251, 255)
        self.size = (30 * randomMultipier, 30 * randomMultipier)  # Width and height of the circle
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = enemySpeed*2
        self.original_image = self.image
        self.maxHealth = math.ceil(maxHealth/2)
        # self.maxHealth = 1
        self.currentHealth = self.maxHealth
        self.damage = self.maxHealth/2
        self.isShooter = False
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


class machineEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemySpeed,maxHealth,randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier
        self.color = (128, 128, 128)
        self.size = (55 * randomMultipier, 55 * randomMultipier)  # Width and height of the circle
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size[0] // 2, self.size[1] // 2), self.size[0] // 2)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.enemySpeed = enemySpeed
        self.original_image = self.image
        self.maxHealth = maxHealth
        self.currentHealth = self.maxHealth
        self.isShooter = True
        self.attackSpeed = 30
        self.attackCooldown = self.attackSpeed
        self.info = pygame.display.Info()
        self.screenWidth = self.info.current_w
        self.screenHeight = self.info.current_h
        self.damage = self.maxHealth/5
        self.outerLimit = random.randint(300, 450)
        self.innerLimit = self.outerLimit - 100
    def shoot(self,playerX,playerY,damage):
        if self.attackCooldown == 0:
            dx = playerX - self.rect.center[0]
            dy = playerY - self.rect.center[1]
            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
            projectile = ememy_projectile_class.machineProjectile(self.rect.center[0],self.rect.center[1],angle,5,damage)
            self.attackCooldown = self.attackSpeed
            return projectile

    def move(self,playerX,playerY,enemies):

        dx = playerX - self.rect.x
        dy = playerY - self.rect.y
        distance = math.hypot(dx, dy)

        if distance < self.innerLimit:
            direction = -1
        elif distance > self.outerLimit:
            direction = 1
        else:
            direction = 0


        move_x = direction * (self.enemySpeed if dx > 0 else -self.enemySpeed)
        move_y = direction * (self.enemySpeed if dy > 0 else -self.enemySpeed)

        if move_x != 0 and move_y != 0:
            length = math.hypot(move_x, move_y)
            move_x = (move_x / length) * self.enemySpeed
            move_y = (move_y / length) * self.enemySpeed


        for enemy in enemies:
            if enemy == self:
                continue
            dx = self.rect.x - enemy.rect.center[0]
            dy = self.rect.y - enemy.rect.center[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance < 100:
                if distance > 0:
                    repulsion_force = 1 / distance
                    move_x += dx * repulsion_force
                    move_y += dy * repulsion_force



        if self.rect.y > self.screenHeight - 40:
            move_y = -5
        if self.rect.x > self.screenWidth - 40:
            move_x = -5
        if self.rect.y < 5:
            move_y = 5
        if self.rect.x < 5:
            move_x = 5


        self.rect.x += move_x
        self.rect.y += move_y


class laserEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemySpeed, maxHealth, randomMultipier):
        pygame.sprite.Sprite.__init__(self)
        self.sizeMultipier = randomMultipier
        self.color = (255,0,0)
        self.size = (40 * randomMultipier, 40 * randomMultipier)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        points = [
            (self.size[0] // 2, 0),(0, self.size[1]),(self.size[0], self.size[1])]
        pygame.draw.polygon(self.image, self.color, points)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        # Save the original image for rotation (always in the upward orientation).
        self.original_image = self.image.copy()
        self.enemySpeed = enemySpeed
        self.original_image = self.image
        self.maxHealth = maxHealth
        self.currentHealth = self.maxHealth
        self.isShooter = True
        self.attackSpeed = 300
        self.attackCooldown = self.attackSpeed

        self.laser_duration = 60
        self.laser_active = False
        self.laser_timer = 0
        self.current_laser = None

        self.info = pygame.display.Info()
        self.screenWidth = self.info.current_w
        self.screenHeight = self.info.current_h
        self.damage = self.maxHealth
        self.outerLimit = random.randint(300, 450)
        self.innerLimit = self.outerLimit - 100
        self.start_pos = 0
        self.end_pos = 0

    def compute_extended_endpoint(self, start_pos, playerX, playerY):
        x0, y0 = start_pos
        dx = playerX - x0
        dy = playerY - y0
        dist = math.hypot(dx, dy)
        if dist == 0:
            return (playerX, playerY)
        # Normalize the direction vector.
        d_x = dx / dist
        d_y = dy / dist

        t_values = []
        # Left wall (x = 0)
        if d_x < 0:
            t_values.append((0 - x0) / d_x)
        # Right wall (x = self.screenWidth)
        if d_x > 0:
            t_values.append((self.screenWidth - x0) / d_x)
        # Top wall (y = 0)
        if d_y < 0:
            t_values.append((0 - y0) / d_y)
        # Bottom wall (y = self.screenHeight)
        if d_y > 0:
            t_values.append((self.screenHeight - y0) / d_y)

        t = min(t_values) if t_values else dist
        extended_x = x0 + t * d_x
        extended_y = y0 + t * d_y
        return extended_x, extended_y
    def update_attack(self):
        if not self.laser_active:
            if self.attackCooldown > 0:
                self.attackCooldown -= 1
            if self.attackCooldown <= 0:
                self.laser_active = True
                self.laser_timer = self.laser_duration
        else:
            self.laser_timer -= 1
            if self.laser_timer <= 0:
                self.laser_active = False
                self.attackCooldown = self.attackSpeed
                if self.current_laser:
                    self.current_laser.kill()
                    self.current_laser = None

    def shoot(self, playerX,playerY,damage):
        self.update_attack()
        if self.attackCooldown > 60:
            cx, cy = self.rect.center
            theta = math.atan2(playerY - cy, playerX - cx)
            tip_offset_x = (self.size[1] / 2) * math.cos(theta)
            tip_offset_y = (self.size[1] / 2) * math.sin(theta)
            self.start_pos = (cx + tip_offset_x, cy + tip_offset_y)
            self.end_pos = self.compute_extended_endpoint(self.start_pos,playerX, playerY)
        if self.laser_active:
            if self.current_laser is None:
                self.current_laser = ememy_projectile_class.Laser(self.start_pos, self.end_pos,damage)
            else:
                # self.current_laser.update(start_pos, end_pos)
                self.current_laser.timer = self.laser_timer
            return self.current_laser
        else:
            if self.current_laser is not None:
                self.current_laser.kill()
                self.current_laser = None
            return None

    def move(self, playerX, playerY, enemies):
        if not self.laser_active and self.attackCooldown > 30:
            dx = playerX - self.rect.x
            dy = playerY - self.rect.y
            distance = math.hypot(dx, dy)

            if distance < self.innerLimit:
                direction = -1
            elif distance > self.outerLimit:
                direction = 1
            else:
                direction = 0

            move_x = direction * (self.enemySpeed if dx > 0 else -self.enemySpeed)
            move_y = direction * (self.enemySpeed if dy > 0 else -self.enemySpeed)

            if move_x != 0 and move_y != 0:
                length = math.hypot(move_x, move_y)
                move_x = (move_x / length) * self.enemySpeed
                move_y = (move_y / length) * self.enemySpeed

            for enemy in enemies:
                if enemy == self:
                    continue
                diff_x = self.rect.x - enemy.rect.center[0]
                diff_y = self.rect.y - enemy.rect.center[1]
                distance_between = math.hypot(diff_x, diff_y)
                if distance_between < 100 and distance_between > 0:
                    repulsion_force = 1 / distance_between
                    move_x += diff_x * repulsion_force
                    move_y += diff_y * repulsion_force

            self.rect.x += move_x
            self.rect.y += move_y

            vec_x = playerX - self.rect.centerx
            vec_y = playerY - self.rect.centery
            desired_rotation = math.degrees(math.atan2(vec_y, vec_x)) + 90
            rotated_image = pygame.transform.rotate(self.original_image, -desired_rotation)
            self.image = rotated_image
            self.rect = self.image.get_rect(center=self.rect.center)


def getEnemy(enemyX,enemyY,randomMultipier,enemyHealth,enemySpeed):
    enemies = {}
    enemies[0] = (Enemy(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    enemies[1] = (greenEnemy(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    enemies[2] = (enemyTank(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    enemies[3] = (healerEnemy(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    enemies[4] = (purpleEnemy(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    enemies[5] = (orangeEnemy(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    enemies[6] = (fastEnemy(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    enemies[7] = (machineEnemy(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    enemies[8] = (laserEnemy(enemyX, enemyY, enemySpeed, enemyHealth, randomMultipier))
    return enemies
