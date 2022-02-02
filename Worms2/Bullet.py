from defaults import *
from math import *

screen = pygame.display.set_mode(SIZE)


class Bullet:
    def __init__(self, x, y,radius=BULLET_CIRCLE_RADIUS, color=GREEN):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius - 1)


    def get_circle_rect(self, screen):
        return pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)

    def ballPath(startx, starty, power, ang, time):
        angle = ang
        velx = cos(angle) * power
        vely = sin(angle) * power

        distX = velx * time
        distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

        newx = round(distX + startx)
        newy = round(starty - distY)


        return (newx, newy)