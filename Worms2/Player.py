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

        self.current_health = 100
        self.target_health = 100
        self.maximum_health = 100
        self.health_bar_length = 40
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = 0.5

        self.is_jumping = False
        self.is_falling = False
        self.jumpCount = 20

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

        if key[pygame.K_x]:
            self.is_jumping = True

        # print test
        # elif key[pygame.K_SPACE]:
        # print("oui")

        pygame.time.delay(5)

    def update(self, aimpoint: AimPoint, screen):

        # Update aimpoint coordinates
        aimpoint.x, aimpoint.y = self.get_aimpoint_coordinates()
        self.basic_health(screen)
        # self.advanced_health(screen)

        if self.is_jumping:
            if self.jumpCount >= -20:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1

                self.rect.y -= (self.jumpCount ** 2) * 0.05 * neg
                self.jumpCount -= 1

            else:
                self.jumpCount = 20
                self.is_jumping = False



    def gravity(self):
        if self.rect.y < 690:
            self.rect.y -= ((-4.9) / 1.25)
        if self.rect.y >= 690:
            self.rect.y = 690
            self.v = 5
            self.is_jumping = False

    def draw(self, screen, color):

        # rect to redraw
        pygame.draw.rect(screen, color, self.rect, 1)

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health

    def basic_health(self, screen):
        pygame.draw.rect(screen, RED, (self.rect.x - 3.5, self.rect.y - 15, self.target_health / self.health_ratio, 5))
        pygame.draw.rect(screen, BLACK, (self.rect.x - 3.5, self.rect.y - 15, self.health_bar_length, 5), 1)

    def advanced_health(self, screen):
        transition_width = 0
        transition_color = RED

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = GREEN

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = YELLOW

        health_bar_rect = pygame.Rect(self.rect.x - 3.5, self.rect.y - 15, self.current_health / self.health_ratio, 5)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, self.rect.y - 15, transition_width, 5)

        pygame.draw.rect(screen, RED, health_bar_rect)
        pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, BLACK, (self.rect.x - 3.5, self.rect.y - 15, self.health_bar_length, 5), 1)
