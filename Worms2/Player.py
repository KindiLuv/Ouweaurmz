import pygame
from pygame.locals import *
import time
from math import *

from AimPoint import *
from Bullet import *

from defaults import *

screen = pygame.display.set_mode(SIZE)


class Player(object):
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect((x, y, RECT_WIDTH, RECT_HEIGHT))

        self.direction = "right"
        self.shooting_angle = pi / 4
        self.change_angle = 0

    def get_aimpoint_coordinates(self):

        if self.direction == "right":
            gunpoint_x = self.rect.x + 30 + int(AIMPOINT_RADIUS * cos(self.shooting_angle))

        else:
            gunpoint_x = self.rect.x - int(AIMPOINT_RADIUS * cos(self.shooting_angle))

        gunpoint_y = self.rect.y - int(AIMPOINT_RADIUS * sin(self.shooting_angle))

        return gunpoint_x, gunpoint_y

    def move(self, event):

        key = pygame.key.get_pressed()

        # horizontal moves
        if key[pygame.K_RIGHT]:
            self.rect.x += 1
            self.direction = "right"
        if key[pygame.K_LEFT]:
            self.rect.x -= 1
            self.direction = "left"

        # Aiming moves
        elif key[pygame.K_UP]:
            self.shooting_angle += SHOOTING_ANGLE_CHANGE
            if self.shooting_angle >= pi / 2:
                self.shooting_angle = pi / 2
        elif key[pygame.K_DOWN]:
            self.shooting_angle += -SHOOTING_ANGLE_CHANGE
            if self.shooting_angle <= -pi / 6:
                self.shooting_angle = -pi / 6

        pygame.time.delay(5)

    def update(self, aimpoint: AimPoint):

        # Update aimpoint coordinates
        aimpoint.x, aimpoint.y = self.get_aimpoint_coordinates()

    def draw(self, screen, color):

        # rect to redraw
        pygame.draw.rect(screen, color, self.rect, 1)
