import pygame
from pygame.locals import *

from defaults import *

pygame.init()
screen = pygame.display.set_mode(SIZE)

rect = Rect(50, 690, RECT_WIDTH, RECT_HEIGHT)
rectCopy = rect.copy()

#rect info
print(f'x={rect.x}, y={rect.y}, w={rect.w}, h={rect.h}')
print(f'left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}')
print(f'center={rect.center}')

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    key = pygame.key.get_pressed()

    if key[pygame.K_RIGHT]:
        rect.x += 5

    screen.fill(GRAY)
    pygame.draw.rect(screen, RED, rect, 1)
    pygame.display.flip()

pygame.quit()