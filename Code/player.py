import pygame as pg
import random

from Code.particle import FlyParticle, FromToParticle
from Code.projectile import Projectile, ChargeProjectile
from Code.functions import random_value, Sound

class Player (pg.sprite.Sprite):
    def __init__(self, pos: tuple[int], group: pg.sprite.Group, projectile_group: pg.sprite.Group):
        super().__init__(group)
        
        self.speed_factor = 0.02
        self.gun_distance = 13
        self.max_speed = 5
        self.hearts = 3
        self.score = 0
        self.reload_speed = 0.3
        self.charge_reload_speed = 2
        self.charge_begin = 0.6
        self.particle_spawn = 0.05
        self.fade_rocket_sound = 3
        self.immunity_time = 1
        
        self.rocket_sound = Sound("Sounds\\Effects\\rocket.wav", 1)
        
        self.shoot_sounds = [
            Sound("Sounds\\Effects\\shoot_1.wav", 3, 0.3), 
            Sound("Sounds\\Effects\\shoot_2.wav", 3, 0.3), 
            Sound("Sounds\\Effects\\shoot_3.wav", 3, 0.3)
        ]
        
        self.charge__shoot_sound = Sound("Sounds\\Effects\\shoot_power.wav", 3, 0.6)
        
        self.image = pg.image.load("Graphics\\spaceship.png")
        self.rect = self.image.get_rect(center = pos)
        self.direction = pg.math.Vector2(0,0)
        self.pos = pg.math.Vector2(self.rect.center)
        self.group = group
        
        self.projectiles = projectile_group
        self.reload = 0
        self.charge = 0
        self.particle = 0
        self.immunity = 0
        self.shoot_ready = False

    def sound(self, dt):
        if self.rocket_sound.is_done(): self.rocket_sound.play()
        volume = self.rocket_sound.get_volume() + dt * self.fade_rocket_sound if self.speed > self.max_speed * 0.4 else self.rocket_sound.get_volume() - dt * self.fade_rocket_sound
        self.rocket_sound.set_volume(max(0.2, volume))
        
    def input(self, dt):
        self.reload += dt
        self.particle += dt
        self.direction = pg.Vector2(pg.mouse.get_pos()[0] - self.pos.x, pg.mouse.get_pos()[1] - self.pos.y)
        self.speed = min(self.direction.magnitude() * self.speed_factor, self.max_speed)
        
        FlyParticle(self.pos, self.group, self.speed)
        
        if pg.mouse.get_pressed()[0]: 
            self.charge += 4 * dt
            if self.charge > self.charge_begin:
                if self.particle > self.particle_spawn: 
                    FromToParticle(self.pos + 0.05 * (self.gun_distance - self.charge_begin) * self.charge * pg.Vector2(random_value(100), random_value(100)), self.pos, self.group, 0.2)
            elif 0 < self.reload: self.shoot_ready = True
        else: self.charge = self.charge - dt if self.charge > 0 else self.charge + dt
        
        if not pg.mouse.get_pressed()[0] and self.reload > self.reload_speed and self.shoot_ready: 
            self.reload = 0
            self.charge = 0 if self.charge > 0 else self.charge
            random.choice(self.shoot_sounds).play()
            Projectile(self.pos, self.gun_distance, self.projectiles)
            Projectile(self.pos, -self.gun_distance, self.projectiles)
            self.shoot_ready = False
        
        if pg.mouse.get_pressed()[0] and self.charge > self.charge_reload_speed:
            self.charge = -self.charge_reload_speed * 2
            self.charge__shoot_sound.play()
            self.reload = -self.reload_speed
            self.shoot_ready = False
            ChargeProjectile(self.pos, self.projectiles)
            
        self.particle = 0 if self.particle > self.particle_spawn else self.particle


    def movement(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        
    def update(self, dt):
        if self.immunity > 0: self.immunity -= dt
        self.input(dt)
        self.sound(dt)
        self.movement(dt)