import pygame
from pygame.locals import *

from Bullet import *
from Player import *
from AimPoint import *
from defaults import *
from Environment import *

from random import *

pygame.init()

# Personnages sprites
player1Sprite = pygame.image.load("img/Frog_1.png")
player2Sprite = pygame.image.load("img/Foxxo_1.png")
crateSprite = pygame.image.load("img/Crate.png")

screen = pygame.display.set_mode(SIZE)

player1 = Player(50, 300)
player2 = Player(950, 300)
aimpoint1 = AimPoint(player1.rect.x + 15, player1.rect.y - 15, RED)
aimpoint2 = AimPoint(player2.rect.x + 15, player2.rect.y - 15, GREEN)

# Environnement setup
EnvironmentList = []
for i in range(30):
    environment = Environment(0 + 50 * i, 670, GREEN)
    environment2 = Environment(50 + 50 * (i * 2), 620, GREEN)
    EnvironmentList.append(environment)
    EnvironmentList.append(environment2)

bullet = Bullet(-10, -10, 5, (255, 255, 255))

bullet_list = pygame.sprite.Group()


def findAngle(pos):
    # ici le projo est au centre du joueur
    sX = bullet.x
    sY = bullet.y
    try:
        # calul de l'angle entre le projo(le centre du joueur) et le viseur (vérifie si le sinus = 0)
        angle = atan((sY - pos[1]) / (sX - pos[0]))
    except:
        # si le calcul de l'angle n'est pas possible c'est que c'est pi/2
        angle = pi / 2

    if pos[1] < sY and pos[0] > sX:
        # viseurY < projoY et viseurX > projoX veut dire qu'on doit retourner la valeur absolue car on est en bas à droite du cercle trigonométrique
        # (si le joueur vise en bas à droite du cercle trigo)
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        # (si le joueur vise en bas à gauche du cercle trigo)
        # pi - angle pour avoir sinus positif sur le cercle trigo
        angle = pi - angle
    elif pos[1] > sY and pos[0] < sX:
        # (si le joueur vise en haut à gauche)
        # pi + angle car il est déjà positif
        angle = pi + angle
    elif pos[1] > sY and pos[0] > sX:
        # (si le joueur vise en haut à droite)
        # pi * 2 pour être à droite du cercle + l'angle pour le sinus
        angle = (pi * 2) + angle

    return angle

running = True
time = 0
power = 0
angle = 0
wind = randint(-20, 20) / 10
shootBullet = False
clock = pygame.time.Clock()
turn = "p1"
while running:
    clock.tick(200)

    if shootBullet:
        if bullet.y < 750 - bullet.radius:
            if turn == "p1":
                # chaque frame le x et le y de la ball sont calculés à +0.05 secondes
                time += 0.05
                po = Bullet.ballPath(bullet, player1.rect.center[0], player1.rect.center[1], power, angle, time, wind)
                bullet.x = po[0]
                bullet.y = po[1]
                if bullet.get_circle_rect(screen).colliderect(player2.rect):
                    player2.get_damage(10)
                    bullet.y = 1000
            else:
                time += 0.05
                po = Bullet.ballPath(bullet, player2.rect.center[0], player2.rect.center[1], power, angle, time, wind)
                bullet.x = po[0]
                bullet.y = po[1]
                if bullet.get_circle_rect(screen).colliderect(player1.rect):
                    player1.get_damage(10)
                    bullet.y = 1000
        else:
            shootBullet = False
            time = 0
            bullet.x = -10
            bullet.y = -10
            if turn == "p1":
                turn = "p2"
                wind = randint(-20, 20) / 10
            else:
                turn = "p1"
                wind = randint(20, 20) / 10

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if not shootBullet:
                    if turn == "p1":
                        # on set la position du projo au centre du joueur pour le find angle
                        bullet.x = player1.rect.center[0]
                        bullet.y = player1.rect.center[1]
                        x = bullet.x
                        y = bullet.y
                        # on set pos au viseur pour le find angle également
                        pos = player1.get_aimpoint_coordinates()
                        shootBullet = True
                        power = 50
                        angle = findAngle(pos)
                    else:
                        bullet.x = player2.rect.center[0]
                        bullet.y = player2.rect.center[1]
                        x = bullet.x
                        y = bullet.y
                        pos = player2.get_aimpoint_coordinates()
                        shootBullet = True
                        power = 50
                        angle = findAngle(pos)

    screen.fill(GRAY)
    font = pygame.font.SysFont(None, 24)
    if wind > 0:
        img = font.render('Right -> ' + str(int(wind * 10)), True, RED)
    if wind < 0:
        img = font.render('Left -> ' + str(int(-wind * 10)), True, RED)
    if wind == 0:
        img = font.render('No wind', True, RED)
    screen.blit(img, (20, 20))



    if player1.target_health != 0:
        screen.blit(player1Sprite, (player1.rect.x, player1.rect.y))
        player1.update(aimpoint1, screen)
        pygame.draw.circle(screen, aimpoint1.color, (aimpoint1.x, aimpoint1.y), aimpoint1.radius, 1)
    if player2.target_health != 0:
        screen.blit(player2Sprite, (player2.rect.x, player2.rect.y))
        player2.update(aimpoint2, screen)
        pygame.draw.circle(screen, aimpoint2.color, (aimpoint2.x, aimpoint2.y), aimpoint1.radius, 1)

    player1.gravity()
    player2.gravity()

    if not shootBullet:
        if turn == "p1":
            player1.move(event)

        if turn == "p2":
            player2.move(event)
    bullet.draw(screen)

    # Check for destruction of environment
    for env in EnvironmentList:
        if not env.isdestroyed:
            env.draw(screen)
            screen.blit(crateSprite, (env.rect.x, env.rect.y))
            if bullet.get_circle_rect(screen).colliderect(env.rect):
                env.isdestroyed = True
                shootBullet = False
                time = 0
                bullet.x = -10
                bullet.y = -10
                if turn == "p1":
                    turn = "p2"
                else:
                    turn = "p1"

    #Player Collision
    for env in EnvironmentList:
        if player1.rect.colliderect(env) and not env.isdestroyed:
            player1.rect.bottom = env.rect.top
        if player2.rect.colliderect(env) and not env.isdestroyed:
            player2.rect.bottom = env.rect.top




    pygame.display.update()
