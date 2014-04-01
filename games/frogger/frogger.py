#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian
"""

import pygame
import sys


def start_screen():
    # Load music and loop it until the start screen ends.
    pygame.mixer.music.load("data/theme.mp3")
    pygame.mixer.music.play(-1)
    
    black, red = (0, 0, 0), (255, 0, 0)
    start_font = pygame.font.Font("data/emulogic.ttf", 20)
    start_screen = True
    
    while start_screen:
        window.fill(black)
#         myfont = pygame.font.SysFont("Britannic Bold", 40)
        nlabel1 = start_font.render("Welcome", 1, red)
        nlabel2 = start_font.render("to", 1, red)
        nlabel3 = start_font.render("Frogger", 1, red)
        window.blit(nlabel1, (150, 200))
        window.blit(nlabel2, (200, 250))
        window.blit(nlabel3, (150, 300))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                start_screen = False
                pygame.mixer.music.fadeout(2000)
        pygame.display.flip()

def main():    
    while True:

        keys = pygame.key.get_pressed()

        # Map Arrow Keys to movements.
        if keys[pygame.K_LEFT]:
            frog.centerx -= 4
        if keys[pygame.K_RIGHT]:
            frog.centerx += 4
        if keys[pygame.K_UP]:
            frog.centery -= 4
        if keys[pygame.K_DOWN]:
            frog.centery += 4

        window.fill((255, 155, 55))
        frog.clamp_ip(window.get_rect())
        window.fill((55, 155, 255), frog)
        pygame.display.update()

        # Cap the framerate at 60 FPS.
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((446, 512), 0, 32)
    clock = pygame.time.Clock()
    frog = pygame.Rect((0, 0), (32, 32))
    #~ frog = pygame.image.load("data/frog.png")
    start_screen()
    main()
