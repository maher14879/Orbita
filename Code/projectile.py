import pygame as pg
from particle import FromToParticle
from functions import random_value

projectile_image = pg.image.load("Graphics\shoot.png")
charge_projectile_image = pg.image.load("Graphics\charge_shoot.png")

class Projectile (pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, offset: int, group: pg.sprite.Group):
        super().__init__(group)

        self.max_age = 1
        self.projectile_speed = 2
        self.knockback = 0.1
        self.group = group
        
        self.age = 0
        self.image = projectile_image
        self.rect = self.image.get_rect(center = (pos[0] + offset, pos[1]))
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2((0, -1000))
            
    def movement(self, dt):
        self.pos += self.direction * dt * self.projectile_speed
        self.rect.center = self.pos
        
    def update(self, dt):
        self.movement(dt)
        self.age += dt
        FromToParticle(self.pos + (self.age * 0.1 + 0.1) * pg.Vector2(random_value(10), random_value(10)), self.pos, self.group, 0.1, "red")
        if self.age > self.max_age: self.kill()

class ChargeProjectile(pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, group: pg.sprite.Group):
        super().__init__(group)
        self.max_age = 0.7
        self.projectile_speed = 0.8
        self.area_squared = 3000
        self.gravity = 500000
        self.area_gravity = self.area_squared * 30
        
        self.group = group
        self.age = 0
        self.image = charge_projectile_image
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2((0, -1000))
        self.explode = False
        
    def movement(self, dt):
        self.pos += self.direction * dt * self.projectile_speed / ((self.age + 1)**2)
        self.rect.center = self.pos
        
    def update(self, dt):
        if self.age < self.max_age / 2: self.movement(dt)
        self.age += dt
        FromToParticle(self.pos + (self.age + 1) * pg.Vector2(random_value(10), random_value(10)), self.pos, self.group, 0.1)