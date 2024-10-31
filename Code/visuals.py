import pygame as pg
from typing import Any

class BasicVisual(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, pos: tuple[int], time: float, image_path):
        super().__init__(group)
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect(center = pos)
        self.direction = pg.math.Vector2(0,0)
        self.pos = pg.math.Vector2(self.rect.center)
        self.group = group
        self.is_visible = False