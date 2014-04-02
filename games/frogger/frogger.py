#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian
"""

import pygame
import sys


class Obstacle(object):

    def __init__(self, x, y, img, direction):
        self.speed = 10
        self.go_left = direction
        self.x = x
        self.y = y
        self.startpos = (x, y)
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()

    def draw(self):
        # Adjust the position of the obstacle.
        if self.go_left:
            self.x -= 2
        else:
            self.x += 2
        # Reset the object if it moves out of screen.
        if abs(self.x - self.startpos[0]) > 480:
            self.x, self.y = self.startpos
        # And finally draw it.
        window.blit(self.img, (self.x, self.y))

class Car(Obstacle):

    def __init__(self, x, y, img, direction=0):
        super(Car, self).__init__(x, y, img, direction)

class Turtle(Obstacle):

    def __init__(self, x, y, img, direction=0):
        super(Turtle, self).__init__(x, y, img, direction)

class Log(Obstacle):

    def __init__(self, x, y, img, direction=0):
        super(Log, self).__init__(x, y, img, direction)

class Frog(object):

    def __init__(self):
        self.img_f = pygame.image.load("data/frog.png")
        self.img_b = pygame.image.load("data/frog_back.png")
        self.img_l = pygame.image.load("data/frog_left.png")
        self.img_r = pygame.image.load("data/frog_right.png")
        self.status = self.img_f
        self.x = 200
        self.y = 560

    def draw(self):
        self.rect = self.status
        window.blit(self.status, (self.x, self.y))

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


def main():

    background = pygame.image.load("data/background.png")
    clock = pygame.time.Clock()
    f = Frog()
    c1a = Car(440, 520, "data/car_1.png", 1)
    c1b = Car(280, 520, "data/car_1.png", 1)
    c1c = Car(120, 520, "data/car_1.png", 1)
    c2a = Car(0, 480, "data/car_2.png")
    c3a = Car(440, 440, "data/car_3.png", 1)
    c4a = Car(0, 400, "data/car_4.png")
    c5a = Car(440, 370, "data/car_5.png", 1)
    t1a = Turtle(440, 280, "data/turtle_3_full.png", 1)
    L1a = Log(0, 240, "data/tree_small.png")
    L2a = Log(0, 200, "data/tree_big.png")
    t2a = Turtle(440, 160, "data/turtle_2_full.png", 1)
    L3a = Log(0, 120, "data/tree_medium.png")

    while True:
        # Draw the images.
        window.blit(background, (0, 0))
        objects = [f, c1a, c1b, c1c, c2a, c3a, c4a, c5a, t1a, t2a,
                   L1a, L2a, L3a]
        for i in objects:
            i.draw()
#             i.rect.clamp_ip(game_zone)

        # Flip the buffer every 60 ms.
        pygame.display.flip()
        clock.tick(30)

        # Main event loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    f.left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    f.right()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    f.forward()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    f.back()
                if event.key == pygame.K_SPACE:
                    print f.x, f.y


if __name__ == '__main__':
    # Initialize Pygame and Window to draw in.
    pygame.init()
    window = pygame.display.set_mode((480, 600), 0, 32)
    game_zone = window.get_rect()
    # ~ frog = pygame.image.load("data/frog.png")
    start_screen()
    main()
