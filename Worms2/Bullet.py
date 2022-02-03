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
        return pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius - 1)

    def ballPath(self, startx, starty, power, ang, time):
        #angle est calculé depuis findAngle
        angle = ang

        #vitesse en fonction de l'angle et de la force
        velx = cos(angle) * power
        vely = sin(angle) * power

        #distance en fonction du temps
        distX = velx * time
        distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

        #création du prochain point dans le temps
        newx = round(startx + distX)
        newy = round(starty - distY)


        return (newx, newy)