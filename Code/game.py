import pygame as pg
import sys

from Code.level import Level
from Code.functions import save, load

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(pg.display.get_desktop_sizes()[0])
        pg.display.set_caption("Orbita")
        pg.display.set_icon(pg.image.load("Graphics\SpaceShip.png"))
        self.clock = pg.time.Clock()
        self.level = Level(load())
        
        pg.mixer.init()
        
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    save(self.level.state)
                    pg.quit()
                    sys.exit()
            if pg.key.get_pressed()[pg.K_ESCAPE]:
                pg.display.iconify()
                    
            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pg.display.update()