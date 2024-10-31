import pygame as pg

from player import Player
from functions import Sound

class BasicShip(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int], group: pg.sprite.Group, projectile_group: pg.sprite.Group, player: pg.sprite):
        super().__init__(group)
        self.speed_factor = 0.02
        self.gun_distance = 13
        self.max_speed = 30
        self.hearts = 3
        self.aggressive = False
        
        self.image = pg.image.load("Graphics\\enemy_ship.png")
        self.rect = self.image.get_rect(center = pos)
        self.direction = pg.math.Vector2(0,0)
        self.pos = pg.math.Vector2(self.rect.center)
        self.group = group
        self.player: Player = player
        
        self.projectiles = projectile_group
        self.reload = 0
    
    def movement(self, dt):
        self.player.pos 
        self.pos += self.direction * self.speed_factor * dt
        self.rect.center = self.pos
        
    def update(self, dt):
        self.movement(dt)
        
    