#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian
"""

import pygame
import sys


def terminate():
    pygame.quit()
    sys.exit()

def wait_for_input():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # pressing escape quits
                    terminate()
                return

def start_screen():
    # Load music and loop it until the start screen ends.
    pygame.mixer.music.load("data/theme.mp3")
    pygame.mixer.music.play(-1)

    # Draw the start screen with title gif and fonts.
    blue, white = (0, 0, 71), (255, 255, 255)
    start_font = pygame.font.Font("data/emulogic.ttf", 20)
    start_title = pygame.image.load("data/frogger_title.gif")
    window.fill(blue)
    nlabel1 = start_font.render("Press any key", 1, white)
    nlabel2 = start_font.render("to", 1, white)
    nlabel3 = start_font.render("continue", 1, white)
    window.blit(nlabel1, (110, 300))
    window.blit(nlabel2, (215, 350))
    window.blit(nlabel3, (160, 400))
    window.blit(start_title, (60, 150))

    # Update the screen only once.
    pygame.display.flip()

    wait_for_input()
    pygame.mixer.music.fadeout(2000)

def main():
    while True:
        # Cap the framerate at 60 FPS.
        clock = pygame.time.Clock()
        clock.tick(30)

        background = pygame.image.load("data/background.png")
        window.blit(background, (0, 0))

        frog = pygame.Rect((0, 0), (32, 32))

        # Map Arrow Keys to movements.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            frog.centerx -= 4
        if keys[pygame.K_RIGHT]:
            frog.centerx += 4
        if keys[pygame.K_UP]:
            frog.centery -= 4
        if keys[pygame.K_DOWN]:
            frog.centery += 4

        window.fill((55, 155, 255), frog)
        pygame.display.update()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == '__main__':
    # Initialize Pygame and Window to draw in.
    pygame.init()
    window = pygame.display.set_mode((480, 600), 0, 32)

    # ~ frog = pygame.image.load("data/frog.png")
    start_screen()
    main()
