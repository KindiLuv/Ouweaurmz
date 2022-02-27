import pygame
from pygame.locals import *
from defaults import *

screen = pygame.display.set_mode(SIZE)


class Environment:

    def __init__(self, x, y, color):
        self.rect = pygame.rect.Rect((x, y, 50, 50))
        self.x = x
        self.y = y
        self.color = color
        self.isdestroyed = False

    def draw(self, ascreen):
        pygame.draw.rect(ascreen, self.color, self.rect)


    def destroyenv(self):
        self.isdestroyed = True
