#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian
"""

import pygame
import sys


class Frog(object):

    def __init__(self, screen):
        self.img_f = pygame.image.load("data/frog.png")
        self.img_b = pygame.image.load("data/frog_back.png")
        self.img_l = pygame.image.load("data/frog_left.png")
        self.img_r = pygame.image.load("data/frog_right.png")
        self.status = self.img_f
        self.screen = screen
        self.x = 200
        self.y = 560

    def draw(self):
        self.screen.blit(self.status, (self.x, self.y))

    def left(self):
        self.status = self.img_l
        self.x -= 40

    def right(self):
        self.status = self.img_r
        self.x += 40


    def forward(self):
        self.status = self.img_f
        self.y -= 40


    def back(self):
        self.status = self.img_b
        self.y += 40



def wait_for_input():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # pressing escape quits
                    terminate()
                return

def terminate():
    pygame.quit()
    sys.exit()

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


def pause():
    pause_font = pygame.font.Font("data/emulogic.ttf", 20)
    pause_label = pause_font.render("paused", 1, (255, 255, 255))
    window.blit(pause_label, (180, 300))
    pygame.display.flip()
    print "pause"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # pressing escape quits
                    return


def main():

    background = pygame.image.load("data/background.png")
    clock = pygame.time.Clock()
    f = Frog(window)

    while True:
        window.blit(background, (0, 0))
        f.draw()
        pygame.display.flip()  # Flips the buffer to show the new screen.
        clock.tick(60)  # Pause for 60 ms.

        # Main event loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_LEFT:
                    f.left()
                if event.key == pygame.K_RIGHT:
                    f.right()
                if event.key == pygame.K_UP:
                    f.forward()
                if event.key == pygame.K_DOWN:
                    f.back()
                print f.x, f.y


if __name__ == '__main__':
    # Initialize Pygame and Window to draw in.
    pygame.init()
    window = pygame.display.set_mode((480, 600), 0, 32)

    # ~ frog = pygame.image.load("data/frog.png")
    start_screen()
    main()
