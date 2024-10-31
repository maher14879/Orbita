import pygame as pg
import os

class Animation():
    def __init__(self, group: pg.sprite.Group):
        animation_frames = {}
        for animation_folder_name in os.listdir("Graphics//Animations"):
            for image_name in os.listdir("Graphics//Animations//" + animation_folder_name):
                if image_name.endswith(".png"):
                    image_path = "Graphics//Animations//" + animation_folder_name + "//" + image_name
                    if not animation_folder_name in animation_frames.keys(): animation_frames[animation_folder_name] = [AnimationFrame(group, pg.image.load(image_path))]
                    else: animation_frames[animation_folder_name] += [AnimationFrame(group, pg.image.load(image_path))]
        self.animation_frames = animation_frames
        self.animations_queue = []
        
        self.frame_rate = 1 / 36
    
    def add_animation(self, pos: tuple[int], animation_folder_name: str):
        animation_frames: list[AnimationFrame] = self.animation_frames[animation_folder_name]
        self.animations_queue.append((pos, animation_frames, 0))
        
    def update(self, dt):        
        def do_animation(pos: tuple[int], frames: list[AnimationFrame], time: float):
            if not len(frames) > 0: return None
            head, *tail = frames
            head.rect.center = pos
            head.is_visible = True
            time += dt
            if time > self.frame_rate:
                head.is_visible = False
                return (pos, tail, time - self.frame_rate)
            else: return (pos, frames, time)
        
        self.animations_queue = [animation for pos, animation_frames, time in self.animations_queue if (animation := do_animation(pos, animation_frames, time))]
    
class AnimationFrame(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, image: pg.Surface):
        super().__init__(group)
        
        self.image = image
        self.rect = self.image.get_rect(center = (0,0))
        self.pos = pg.math.Vector2(self.rect.center)
        self.group = group
        self.is_visible = False