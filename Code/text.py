import pygame as pg
pg.font.init()
font = pg.font.Font("Graphics\\fonts\\8bitOperatorPlus8-Bold.ttf", 32)

class Text():
    def __init__(self, pos: tuple[int], text: str, topleft: bool = True):
        self.text = font.render(text, True, "grey")
        self.rect = self.text.get_rect(topleft = pos) if topleft else self.text.get_rect(center = pos)