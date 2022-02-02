import pygame
from pygame.locals import *

from Bullet import *
from Player import *
from AimPoint import *
from defaults import *

pygame.init()

screen = pygame.display.set_mode(SIZE)

player = Player()
aimpoint = AimPoint(player.rect.x + 15, player.rect.y - 15)

bullet_list = pygame.sprite.Group()


def findAngle(pos):
    sX = bullet.x
    sY = bullet.y
    try:
        angle = atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (pi * 2) - angle

    return angle

bullet = Bullet(0, 0, 5, (255, 255, 255))

running = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()
while running:
    clock.tick(200)
    if shoot:
        if bullet.y < 750 - bullet.radius:
            time += 0.05
            po = Bullet.ballPath(player.rect.center[0], player.rect.center[1], power, angle, time)
            bullet.x = po[0]
            bullet.y = po[1]
        else:
            shoot = False
            time = 0
            bullet.x = 0
            bullet.y = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                bullet.x = player.rect.center[0]
                bullet.y = player.rect.center[1]
                x = bullet.x
                y = bullet.y
                pos = player.get_aimpoint_coordinates()
                shoot = True
                power = 50
                angle = findAngle(pos)

    screen.fill(GRAY)
    player.draw(screen)
    pygame.draw.circle(screen, aimpoint.color, (aimpoint.x, aimpoint.y), aimpoint.radius, 1)
    if not shoot:
        player.move(event)
    player.update(aimpoint)
    bullet.draw(screen)
    pygame.display.update()
