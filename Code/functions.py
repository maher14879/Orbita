import pygame as pg
import random
import json

#from particle import FromToParticle #debug

pg.mixer.init()

def random_value(x):
    return result if (result:=random.randint(-x, x)) else random_value(x)

class Sound():
    def __init__(self, file_path: str, channel: int = 7, volume: float = 1):
        self.channel = pg.mixer.Channel(channel)
        self.sound = pg.mixer.Sound(file_path)
        self.sound.set_volume(volume)
        
    def play(self):
        self.channel.stop()
        self.channel.play(self.sound)
    
    def set_volume(self, volume: float): self.channel.set_volume(volume)
    def get_volume(self): return self.channel.get_volume()
    def stop(self): self.channel.stop()
    def is_done(self): return not self.channel.get_busy()
    def fade_out(self, time): self.channel.fadeout(time)

class AsteroidVector():
    def __init__(self, particle_group: pg.sprite.Group, displayX: float, displayY: float, rotate_speed: float):
        self.center = pg.Vector2(displayX, displayY) * 0.5
        self.vector = pg.Vector2(displayX, displayY) * 0.2
        self.pos = pg.Vector2((0,0))
        self.rotate_speed = rotate_speed
        #self.particle_group = particle_group #debug
    
    def update(self, dt):
        self.vector = self.vector.rotate(360 * dt / self.rotate_speed)
        self.pos = self.center + self.vector
        #FromToParticle(self.pos - pg.Vector2(random_value(10), random_value(10)), self.pos, self.particle_group, 0.1) #debug
        
def save(state_list: dict):
    with open("Save\\settings.json", "w") as file: json.dump(state_list, file)
    
def load() -> dict:
    try: 
        with open("Save\\settings.json", "r") as file: return dict(json.load(file)) 
    except: 
        with open("Save\\settings.json", "w") as file: json.dump({}, file)
        return {}
    