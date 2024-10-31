import pygame as pg
import random
import math

from player import Player
from projectile import Projectile, ChargeProjectile
from particle import LightParticle, ColorParticle, RotateParticle, StarParticle
from asteroid import Asteroid, Orb
from animation import Animation, AnimationFrame
from visuals import BasicVisual
from text import Text
from enemy import BasicShip

from functions import Sound, AsteroidVector, load

class Level:
    def __init__(self, state: dict):
        self.display_surface = pg.display.get_surface()
        self.displayX = self.display_surface.get_size()[0]
        self.displayY = self.display_surface.get_size()[1]
        
        self.ship_sprites: pg.sprite.Group[Player] = pg.sprite.Group()
        self.enemy_ship_sprites: pg.sprite.Group[BasicShip] = pg.sprite.Group()
        self.asteroid_sprites: pg.sprite.Group[Asteroid] = pg.sprite.Group()
        self.projectile_sprites: pg.sprite.Group[Projectile|ChargeProjectile] = pg.sprite.Group()
        self.background_sprites: pg.sprite.Group[LightParticle|StarParticle|ColorParticle] = pg.sprite.Group()
        self.foreground_sprites: pg.sprite.Group[AnimationFrame] = pg.sprite.Group()
        
        self.setup(state)
        
    def setup(self, state:dict):
        self.max_score = state["max_score"] if "max_score" in state.keys() else None
        self.player = Player((self.displayX / 2, self.displayY / 2), (self.ship_sprites), self.projectile_sprites)
        self.projectile_explode_sound = Sound("Sounds\\Effects\\projectile_explode.wav", 2)
        self.spaceship_hit = Sound("Sounds\\Effects\\spaceship_hit.wav", 6)

        self.animations = Animation(self.foreground_sprites)
        self.projectile_explode_choice = ["explosion1", "explosion6"]
        self.player_explode = "explosion2"
        self.charge_sound = Sound("Sounds\\Effects\\charge_destroy.wav", 2, 0.5)
 
        pg.mixer.music.load(filename="Sounds\\Music\\vector.mp3") #intro music
        self.gameplay_music = ["Sounds\\Music\\orthonormal.mp3", "Sounds\\Music\\parameter.mp3", "Sounds\\Music\\vector.mp3"]
        self.music_volume = 0.7 
        self.intro_logo = BasicVisual(self.foreground_sprites, (self.displayX / 2, self.displayY / 2), 100, "Graphics\\Logo.png")
        self.intro_flash_time = state["intro_flash_time"] if "intro_flash_time" in state.keys() else 9

        self.spawn_time_star = 0.3
        self.spawn_time_asteroid = 5
        self.max_asteroids = 10
        self.max_weight = 11
        self.asteroid_cluster_weight = 4
        orbit_speed = 8
        self.asteroid_movement_vector = AsteroidVector(self.background_sprites, self.displayX, self.displayY, orbit_speed)
        
        self.asteroid_weights = []
        for i, w in enumerate([(i + 1)**2 for i in range(self.max_weight)]):
            if self.max_weight - i > self.asteroid_cluster_weight: continue
            for _ in range(w): self.asteroid_weights.append(self.max_weight - i)
        
        outro_statement1, outro_statement2 = random.choice([
            ("Hang in there...", "you got this"),
            ("You lose, yet try again...", "thats why others depend on you"),
            ("How does it feel...", "to have so much potential?"), 
            ("You died...",  "but your death inspired others"), 
            ("It will take you long...", "but the time will pass anyway"),
            ("You are tired...", "lie down for a bit"),
            ("You have so much potential...", "you just have to try"),
        ])
        
        self.lose_text1 = Text((self.displayX/2, self.displayY/2), outro_statement1, False)
        self.lose_text2 = Text((self.displayX/2, self.displayY/2), outro_statement2, False)
        self.outro_particle_time = 5
        self.outtro_song = Sound("Sounds\\Ambient\\outtro.ogg")
        
        self.star_time = 0
        self.asteroid_time = 0
            
        self.intro_time = 0
        self.outtro_time = 0
        self.restart = False
        
        self.state = state
        
    def intro(self, dt):
        if self.intro_time == 0: 
            pg.mixer.music.set_volume(self.music_volume)
            pg.mixer.music.play(fade_ms=self.intro_flash_time*1000)
            pg.mixer.music.set_pos(9 - self.intro_flash_time)
            self.intro_flash_time += dt
        self.intro_time += dt
        
        t = self.intro_time
        x = self.displayX
        y = self.displayY
        
        division_factor = 1 / (2 * self.intro_flash_time)
        
        if t < self.intro_flash_time:
            star_pos = (((x / 2 - (x * division_factor) * t) * math.sin(t**2)) + x / 2, 
                        ((y / 2 - (y * division_factor) * t) * math.cos(t**2)) + y / 2)
            ColorParticle(star_pos, self.background_sprites, (pg.math.Vector2((0, 0))), "purple", 10)
        elif t < self.intro_flash_time + 0.1 and len(self.background_sprites) > 0:
            self.display_surface.fill("white")
            self.animations.add_animation((x/2, y/2), "explosion5")
            for sprite in self.background_sprites: sprite.kill()
            self.state["intro_flash_time"] = 2
        else:
            for _ in range(10): RotateParticle((x / 2, y / 2), self.background_sprites)
            
    def outtro(self, dt): 
        if self.outtro_time == 0:
            all_groups = [self.ship_sprites, self.asteroid_sprites, self.background_sprites, self.foreground_sprites, self.projectile_sprites]
            for group in all_groups:
                for sprite in group: 
                    if not type(sprite) == StarParticle: sprite.kill()
            pg.mixer.music.fadeout(1000)
            self.player.rocket_sound.fade_out(10)
            self.outtro_song.play()
            self.outtro_song.fade_out(round(1000 * (self.outro_particle_time * 2 + dt)))
        
        self.outtro_time += dt
        
        if self.outtro_time < self.outro_particle_time:
            self.display_surface.blit(self.lose_text1.text, self.lose_text1.rect)
            RotateParticle((self.player.pos.x, self.player.pos.y), self.background_sprites, max_age=self.outro_particle_time)
        else:
            self.display_surface.blit(self.lose_text2.text, self.lose_text2.rect)
            
        if self.outtro_time > self.outro_particle_time * 2:
            pg.mixer.stop()
            self.setup(load())
            self.intro_flash_time = 3
            
    def collision(self, dt):   
        for projectile in self.projectile_sprites:
            if type(projectile) == Projectile:
                for asteroid in self.asteroid_sprites:
                    if (projectile.pos - asteroid.pos).length() < asteroid.rect.width + 3:
                        self.projectile_sprites.remove(projectile)
                        new_asteroid_direction = asteroid.direction + (projectile.direction * projectile.knockback / asteroid.weight)
                        if asteroid.weight > 1: Asteroid(asteroid.pos, self.asteroid_sprites, self.background_sprites, self.asteroid_movement_vector, asteroid.weight - 1, new_asteroid_direction, asteroid.particle_color)
                        self.asteroid_sprites.remove(asteroid)
                        self.animations.add_animation(asteroid.pos, random.choice(self.projectile_explode_choice))
                        self.projectile_explode_sound.play()
                        Orb(asteroid.pos, self.background_sprites, self.player)
                        
            if type(projectile) == ChargeProjectile:
                kill = False
                for asteroid in self.asteroid_sprites:
                    distance_squared = pg.Vector2.distance_squared_to(asteroid.pos, projectile.pos) 
                    if asteroid.weight >= self.max_weight and distance_squared*2 < asteroid.rect.width**2:
                        self.animations.add_animation(asteroid.pos, "charge_explosion_destroy")
                        self.projectile_explode_sound.play()
                        for _ in range(asteroid.weight): Orb(asteroid.pos + pg.Vector2((random.randint(-1, 1), random.randint(-1, 1))), self.background_sprites, self.player)
                        asteroid.kill()
                        self.charge_sound.play()
                        kill = True
                        break
                                    
                if projectile.age < projectile.max_age / 2: continue
                if not projectile.explode: 
                    self.animations.add_animation(projectile.pos, "charge_explosion_1")
                    projectile.explode = True
                weight_sum = 0
                asteroid_kill_list:pg.sprite.Group[Asteroid] = pg.sprite.Group()
                for asteroid in self.asteroid_sprites:
                    distance_squared = pg.Vector2.distance_squared_to(asteroid.pos, projectile.pos) 
                    
                    if distance_squared < projectile.area_gravity:
                        factor = (1 + projectile.age - projectile.max_age) * projectile.gravity / asteroid.weight
                        asteroid.direction = factor * dt * (projectile.pos - asteroid.pos).normalize()
                        
                    if distance_squared < projectile.area_squared and weight_sum + asteroid.weight <= self.max_weight * 2 and asteroid.weight < self.max_weight:
                        weight_sum += asteroid.weight
                        asteroid_kill_list.add(asteroid)
                        
                if len(asteroid_kill_list) > 1:
                    for asteroid in asteroid_kill_list:
                        self.animations.add_animation(asteroid.pos, "charge_explosion_2")
                        asteroid.kill()
                    if weight_sum > 0: 
                        Asteroid(projectile.pos, self.asteroid_sprites, self.background_sprites, self.asteroid_movement_vector, weight_sum)
                    kill = True
                    
                if kill or projectile.age > projectile.max_age:
                    for asteroid in self.asteroid_sprites:
                        if distance_squared < projectile.area_gravity: 
                            asteroid.direction = pg.Vector2((0,0))
                    projectile.kill()
        for asteroid in self.asteroid_sprites:
            if (self.player.pos - asteroid.pos).magnitude() < (asteroid.rect.width / 2) + 4:
                self.asteroid_sprites.remove(asteroid)
                self.animations.add_animation(asteroid.pos, self.player_explode)
                if not self.player.immunity > 0: 
                    self.player.hearts += -1
                    if self.player.hearts > 1: self.spaceship_hit.play()
                else: self.projectile_explode_sound.play()
                self.player.immunity = self.player.immunity_time
                
    def spawn_stars(self, dt):
        self.star_time += dt
        if self.star_time > self.spawn_time_star: 
            StarParticle((random.randint(0, self.displayX), 0), self.background_sprites, self.player)
            self.star_time = 0
                
    def spawn_objects(self, dt):
        self.asteroid_time += dt
        if self.asteroid_time > self.spawn_time_asteroid: 
            self.asteroid_time = 0
            if len(self.asteroid_sprites) < self.max_asteroids:
                weight_sum = 0
                while weight_sum < self.asteroid_cluster_weight:
                    weight = random.choice(self.asteroid_weights)
                    weight_sum += weight
                    Asteroid((random.randint(0, self.displayX), -10), self.asteroid_sprites, self.background_sprites, self.asteroid_movement_vector, weight)
    
    def scoreboard(self):
        hearts = Text((10, 15), "Hearts: " + " • " * self.player.hearts)
        self.display_surface.blit(hearts.text, hearts.rect)
        
        score_text = "New Max: " if self.max_score and self.max_score < self.player.score else "Score: "
        
        score = Text((10, 55), score_text + str(self.player.score))
        self.display_surface.blit(score.text, score.rect)
        
        if self.max_score and self.max_score >= self.player.score: 
            max_score = Text((10, 95), "Max Score: " + str(self.max_score))
            self.display_surface.blit(max_score.text, max_score.rect)
            
        self.state["max_score"] = self.max_score if self.max_score and self.max_score > self.player.score else self.player.score
        
    def run(self, dt):
        self.display_surface.fill("black")
        
        self.background_sprites.draw(self.display_surface)
        self.background_sprites.update(dt)
        self.asteroid_movement_vector.update(dt)
        
        if not self.intro_time > self.intro_flash_time + 0.5: 
            self.intro(dt)
        elif self.player.hearts > 0:
            self.spawn_stars(dt)
            self.spawn_objects(dt)
            self.collision(dt)
            self.ship_sprites.draw(self.display_surface)
            self.projectile_sprites.draw(self.display_surface)
            self.asteroid_sprites.draw(self.display_surface)
            self.ship_sprites.update(dt)
            self.projectile_sprites.update(dt)
            self.asteroid_sprites.update(dt)
            self.scoreboard()
            if not pg.mixer.music.get_busy():
                if self.gameplay_music:
                    song_path = self.gameplay_music.pop()
                    pg.mixer.music.load(song_path)
                    pg.mixer.music.play()
        else: 
            self.outtro(dt)
        
        self.animations.update(dt)
        pg.sprite.Group([sprite for sprite in self.foreground_sprites if sprite.is_visible]).draw(self.display_surface)