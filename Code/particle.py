import pygame as pg
import random

class FlyParticle (pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, group: pg.sprite.Group, speed: float):
        super().__init__(group)
        
        self.speed_factor = speed * 5
        self.max_age = random.randint(1, round(speed) + 1) * 0.05
        
        self.age = 0
        self.colorChange = 200
        self.image = pg.Surface((3, 3))
        self.image.fill("white")
        self.rect = self.image.get_rect(center = (pos[0], pos[1] + 18))
        self.pos = pg.math.Vector2(self.rect.center)
            
    def movement(self, dt):
        random_factor = round(self.age * self.speed_factor * 0.5)
        self.pos += random.randint(-random_factor, random_factor), self.speed_factor * dt + 1
        self.rect.center = self.pos
        
    def update(self, dt):
        self.movement(dt)
        self.age += dt
        if self.age > self.max_age: self.kill()
        
        self.colorChange = min(200, max(0, abs(250 - (self.age * 200) / self.max_age)))
        self.image.fill((self.colorChange, self.colorChange, self.colorChange))
        
class FromToParticle (pg.sprite.Sprite):
    def __init__(self, start: pg.math.Vector2, end: pg.math.Vector2, group: pg.sprite.Group, max_age: int, color: str = "cyan"):
        super().__init__(group)
        
        self.max_age = max_age
        size = random.randint(1,2)
        
        self.age = 0
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = start)
    
        self.direction = pg.math.Vector2(end - start).normalize()
        self.pos = pg.math.Vector2(self.rect.center)
        
        self.speed = start.distance_to(end) / max_age
            
    def movement(self, dt):
        self.pos += self.direction * dt * self.speed
        self.rect.center = self.pos
    
    def update(self, dt):
        self.movement(dt)
        self.age += dt
        if self.age > self.max_age: self.kill()

class LightParticle (pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, group: pg.sprite.Group, span: int, color: str = "gold"):
        super().__init__(group)
        
        self.max_age = min(10, span)
        
        self.age = 0
        self.image = pg.Surface((span * 5, span * 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = pos)
        
        randomVector = random.randint(-1000,1000)/10, random.randint(-1000,1000)/10
    
        self.direction = pg.math.Vector2(randomVector)
        self.pos = pg.math.Vector2(self.rect.center)
            
    def movement(self, dt):
        self.pos += self.direction * dt
        self.rect.center = self.pos
    
    def update(self, dt):
        self.movement(dt)
        self.age += dt
        if self.age > self.max_age: self.kill()
        
        color = min(200, max(0, (self.max_age - self.age) * 200 / self.max_age))
        self.image.fill((color, color/2, color/4))
        
class ColorParticle(pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, group: pg.sprite.Group, direction: pg.math.Vector2, color_type: str, span: int):
        super().__init__(group)

        scale = random.randint(1,4)
        self.max_age = random.random() * min(10, span) / (scale * 30)
        self.age = 0
        self.image = pg.Surface((scale, scale))
        self.image.fill("gold")
        self.direction = pg.math.Vector2(direction)
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.center)
        self.type_color = color_type
            
    def movement(self, dt):
        self.pos += self.direction * dt
        self.rect.center = self.pos
    
    def update(self, dt):
        self.movement(dt)
        self.age += dt
        
        color = min(200, max(0, (self.max_age - self.age) * 200 / self.max_age))
        if self.type_color == "blue": self.image.fill((color, color, 200))
        if self.type_color == "red": self.image.fill((200 - color, 200 - color, 200))
        if self.type_color == "purple": self.image.fill((color, color/4, 255))
        if self.type_color == "cyan": self.image.fill((0, 255-color, 255-color))
        
        if self.age > self.max_age: self.kill()
        
class RotateParticle(pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, group: pg.sprite.Group, max_age: int = 3):
        super().__init__(group)

        self.scale = random.randint(1,6)
        self.max_age = max_age
        self.age = 0
        self.image = pg.Surface((self.scale, self.scale))
        self.image.fill("black")
        self.direction = pg.math.Vector2(((random.random() - 0.5) * 5000, (random.random() - 0.5) * 5000))
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.center)
        self.type_color = random.choice(["red", "orange"])
            
    def movement(self, dt):
        self.direction = self.direction.rotate(dt * (50 + self.scale * 2))
        self.pos += self.direction * dt
        self.rect.center = self.pos
    
    def update(self, dt):
        self.movement(dt)
        self.age += dt
        
        color = min(200, max(0, (self.max_age - self.age) * 200 / self.max_age))
        if self.type_color == "red": self.image.fill((255, color / 3, color / 6))
        if self.type_color == "orange": self.image.fill((255, color, color / 4))
        if self.age > self.max_age: self.kill()

class StarParticle (pg.sprite.Sprite):
    def __init__(self, pos: pg.math.Vector2, group: pg.sprite.Group, player):
        super().__init__(group)
        
        self.scale = random.randint(1, 100)
        self.age = 0
        
        self.player = player
        
        self.image = pg.Surface((self.scale / 20, self.scale / 20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center = pos)
        self.pos = pg.math.Vector2(self.rect.center)
    
    def update(self, dt):
        self.pos += (-self.scale * self.player.direction.x * 0.01) * dt, (100 - self.scale * self.player.direction.y * 0.01) * dt
        self.rect.center = self.pos
        self.age += dt
        if self.age > self.scale: self.kill()