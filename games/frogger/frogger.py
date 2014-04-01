#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian
"""

import pygame
import sys

pygame.init()
window = pygame.display.set_mode((446, 512), 0, 32)
clock = pygame.time.Clock()
object = pygame.Rect((0, 0), (64, 64))

# Colors and other basic globals:
black = (0, 0, 0)
red = (255, 0, 0)
gamename = "Frogger"
gamefont = pygame.font.Font("data/emulogic.ttf", 20)

def start_screen():
    pygame.mixer.music.load("data/theme.mp3")
    pygame.mixer.music.play(100)
    wait = True
    while wait:
        window.fill(black)
#         myfont = pygame.font.SysFont("Britannic Bold", 40)
        nlabel1 = gamefont.render("Welcome".format(gamename), 1, red)
        nlabel2 = gamefont.render("to", 1, red)
        nlabel3 = gamefont.render("{}".format(gamename), 1, red)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                wait = False
                pygame.mixer.music.fadeout(2000)
        window.blit(nlabel1, (150, 200))
        window.blit(nlabel2, (200, 250))
        window.blit(nlabel3, (150, 300))
        pygame.display.flip()

def main():
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

        window.fill((255, 155, 55))
        object.clamp_ip(window.get_rect())
        window.fill((55, 155, 255), object)
        pygame.display.update()

        # Cap the framerate at 60 FPS.
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == '__main__':
    start_screen()
    main()
