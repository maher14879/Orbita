import pygame as pg
import random

from player import Player
from particle import ColorParticle
from functions import Sound, AsteroidVector

asteroid_images = [pg.image.load("Graphics\\Asteroids\\" + str(i+1) + ".png") for i in range(11)]
orb_images = [pg.image.load("Graphics\\Orbs\\orb_1.png"), pg.image.load("Graphics\\Orbs\\orb_2.png")]
orb_sounds = [Sound("Sounds\\Effects\\collect_orb_1.wav", 4, 0.2),
              Sound("Sounds\\Effects\\collect_orb_2.wav", 4, 0.2),
              Sound("Sounds\\Effects\\collect_orb_3.wav", 4, 0.2)]

class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int], group: pg.sprite.Group, particle_group: pg.sprite.Group, movement_vector: AsteroidVector, weight: int, start_direction: tuple[int] = None, particle_color: str = None):
        super().__init__(group)
        
        asteroid_start_speed = 50
        
        self.movement_vector_pull_factor = 2
        self.gravity = 1000
        self.drag = weight * 0.01 + 0.1
        self.particle_group = particle_group
        self.movement_vector = movement_vector
        self.image = pg.transform.rotate(asteroid_images[min(weight-1, 10)], random.randint(1, 360))
        self.direction:pg.math.Vector2 = (pg.math.Vector2(start_direction) if start_direction else 
                                          pg.math.Vector2(10 * (random.random() - 0.5), asteroid_start_speed))
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.center)
        self.asteroids:list[Asteroid] = group
        self.weight = weight
        self.particle_color = particle_color if particle_color else random.choice(["blue", "red", "purple"])
        self.gravitate = True
    
    def update(self, dt):
        asteroids_count = len(self.asteroids)
        for asteroid in self.asteroids:
            distance = self.pos.distance_squared_to(asteroid.pos)
            if distance > (self.rect.width + asteroid.rect.width)**2:
                factor = (asteroid.weight**2 * self.weight / asteroids_count) / (max(1, distance))
                self.direction += (asteroid.pos - self.pos) * factor * dt * self.gravity
            if 0 < distance < (self.rect.width + asteroid.rect.width)**2: 
                self.direction += (self.pos - asteroid.pos) * dt / (self.weight / asteroids_count)

        distance = self.movement_vector.pos.distance_squared_to(self.pos)
        if distance > (self.rect.width*2)**2:
            self.direction += (self.movement_vector.pos - self.pos) * self.movement_vector_pull_factor * dt
        if self.gravitate and 0 < distance < (self.rect.width*2)**2: 
            self.direction += (self.pos - self.movement_vector.pos) * dt
            
        self.direction = self.direction / (1 + self.drag * dt)
        self.pos += self.direction * dt
        self.rect.center = self.pos
        
        random_position = self.pos + (random.randint(-self.rect.width, self.rect.width) / 2, random.randint(-self.rect.height, self.rect.height) / 2)
        ColorParticle(random_position, self.particle_group, -self.direction, self.particle_color, self.direction.length())
        
class Orb(pg.sprite.Sprite):
    def __init__(self, pos: tuple[int], group: pg.sprite.Group, player: Player, collect_time: float = 1., value:int = 1):
        super().__init__(group)

        self.age = 0
        self.collect_distance = 20
        self.player_pull_factor = 50000
        self.value = value
        self.collect_time = collect_time
        self.despawn_time = 5. + collect_time
        self.player: Player = player
        self.group = group
        self.image = random.choice(orb_images)
        self.direction = pg.math.Vector2(100 * random.random() - 50, 100 * random.random() - 50)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.center)
        self.asteroids:list[Asteroid] = group
        
    def update(self, dt):
        self.age += dt
        if self.age > self.despawn_time: self.kill()
        difference_vector = self.player.pos - self.pos
        distance = difference_vector.length()
        self.collect_time -= dt
        if self.collect_time < 0:
            ColorParticle(self.pos, self.group, (0,0), "cyan", 10)
            if distance < self.collect_distance: 
                self.player.score += self.value
                random.choice(orb_sounds).play()
                self.kill()
            self.direction = (difference_vector * self.player_pull_factor) / max(10, (distance**2))
        self.pos += self.direction * dt
        self.pos += -self.player.direction * dt
        self.rect.center = self.pos
