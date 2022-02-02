from defaults import *

screen = pygame.display.set_mode(SIZE)


class AimPoint:
    def __init__(self, x, y, color, radius=AIMPOINT_CIRCLE_RADIUS):
        self.circle = pygame.draw.circle(screen, color, (x, y), radius)
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)