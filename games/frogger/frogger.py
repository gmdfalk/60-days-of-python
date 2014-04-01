"""
    Created on 1 Apr 2014

    @author: Max Demian
"""

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
clock = pygame.time.Clock()
object = pygame.Rect((0, 0), (64, 64))

while True:
    keys = pygame.key.get_pressed()

    # Map Arrow Keys to movements.
    if keys[pygame.K_LEFT]:
        object.centerx -= 4
    if keys[pygame.K_RIGHT]:
        object.centerx += 4
    if keys[pygame.K_UP]:
        object.centery -= 4
    if keys[pygame.K_DOWN]:
        object.centery += 4

    screen.fill((255, 155, 55))
    object.clamp_ip(screen.get_rect())
    screen.fill((55, 155, 255), object)
    pygame.display.update()

    # Cap the framerate at 60 FPS.
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

if __name__ == '__main__':
    pass
