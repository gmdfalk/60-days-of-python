#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian

    Todo:
    * Collision (+Drowning)
    * Home Zone (+img_safe)
    * Timer
    * Animations (Frog + Turtles)
    * Sounds & Music
    * Score and Highscores
"""

import pygame
import sys
from random import choice, randrange, random


class StaticObstacle(object):

    def __init__(self):
        self.y = 80
        self.spawns = [420, 320, 220, 120, 20]
        self.imgs = ["data/croc.png", "data/fly.png"]

    def update(self):
        "Draws at a random spawn point for a random duration"
        self.img = pygame.image.load(choice(self.imgs))
        self.duration = randrange(5, 10)
        window.blit(self.img, (choice(self.spawns), self.y))


class MovingObstacle(object):
    "Base class for all moving obstacles"
    def __init__(self, x, y, img, direction):
        self.speed = 10
        self.go_left = direction
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()

    def update(self):
        "Moves and then draws the obstacle"
        # Adjust the position of the obstacle.
        if self.go_left:
            self.x -= 2
        else:
            self.x += 2
        # Reset the object if it moves out of screen.
        # To accomodate the big logs and introduce gaps, we use -180, not 0.
        if self.x > 480:
            self.x = -180
        elif self.x < -180:
            self.x = 480
        # And finally draw it.
        window.blit(self.img, (self.x, self.y))


class Car(MovingObstacle):

    def __init__(self, x, y, img, direction=0):
        super(Car, self).__init__(x, y, img, direction)


class Turtle(MovingObstacle):

    def __init__(self, x, y, img, direction=0):
        super(Turtle, self).__init__(x, y, img, direction)


class Log(MovingObstacle):

    def __init__(self, x, y, img, direction=0):
        super(Log, self).__init__(x, y, img, direction)


class Frog(object):

    def __init__(self):
        self.img_f = pygame.image.load("data/frog.png")
        self.img_b = pygame.image.load("data/frog_back.png")
        self.img_l = pygame.image.load("data/frog_left.png")
        self.img_r = pygame.image.load("data/frog_right.png")
        self.img_safe = pygame.image.load("data/frog_safe.png")
        self.img_life = pygame.image.load("data/lives.png")
        self.img_empty = pygame.image.load("data/empty.png")
        self.death_imgs = ["data/frog_death_1.png", "data/frog_death_2.png",
                           "data/frog_death_3.png"]
        self.img_death = pygame.image.load(self.death_imgs[2])
        self.status = self.img_f
        self.x = 200
        self.y = 560
        self.lives = 4

    def update(self):
        self.rect = self.status
        window.blit(self.status, (self.x, self.y))

    def left(self):
        self.status = self.img_l
        self.x -= 20

    def right(self):
        self.status = self.img_r
        self.x += 20

    def forward(self):
        self.status = self.img_f
        self.y -= 40

    def back(self):
        self.status = self.img_b
        self.y += 40

    def update_lives(self, reduction=0):
        "Deduct/Add lives and draw the life bar"
        self.lives += reduction
        x, y = 0, 40
        for _ in range(self.lives):
            window.blit(self.img_life, (x, y))
            x += 20

    def death(self):
        "Update lives, trigger visual clues and reset frog position to default"
        self.update_lives(-1)
        self.status = self.img_death
        self.update()
        pygame.display.flip()
        pygame.time.delay(1500)
        self.status = self.img_f
        self.x, self.y = 200, 560


def wait_for_input():
    # Allow these keys to cancel the loop.
    valid_keys = [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key in valid_keys:
                    # Return to wherever we were called from.
                    return


def pause():
    pause_font = pygame.font.Font("data/emulogic.ttf", 20)
    pause_label = pause_font.render("PAUSED", 1, (255, 255, 255))
    window.blit(pause_label, (180, 300))
    pygame.display.flip()
    print "paused"
    wait_for_input()


def game_over():
    gameover_font = pygame.font.Font("data/emulogic.ttf", 20)
    gameover_label = gameover_font.render("GAME OVER", 1, (255, 255, 255))
    window.blit(gameover_label, (150, 300))
    pygame.display.flip()
    wait_for_input()
    terminate()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    "A simple welcome screen with some music"
    # Load music and loop it until the start screen ends.
    pygame.mixer.music.load("data/theme.mp3")
    pygame.mixer.music.play(-1)

    # Draw the start screen with title gif and fonts.
    blue, white = (0, 0, 71), (255, 255, 255)
    start_font = pygame.font.Font("data/emulogic.ttf", 20)
    start_title = pygame.image.load("data/frogger_title.gif")
    window.fill(blue)
    label1 = start_font.render("Press Enter", 1, white)
    label2 = start_font.render("to", 1, white)
    label3 = start_font.render("continue", 1, white)
    window.blit(label1, (140, 300))
    window.blit(label2, (215, 350))
    window.blit(label3, (160, 400))
    window.blit(start_title, (60, 150))

    # Update the screen only once.
    pygame.display.flip()

    wait_for_input()
    pygame.mixer.music.fadeout(2000)


def create_road():
    "Create the Car instances"
    road = []
    ys = [520, 480, 440, 400, 360]
    x = 0
    for _ in range(2):
        car = Car(x, ys[0], "data/car_1.png", 1)
        road.append(car)
        x += 144
    x = 20
    for _ in range(3):
        car = Car(x, ys[1], "data/car_2.png")
        road.append(car)
        x += 128
    x = 40
    for _ in range(3):
        car = Car(x, ys[2], "data/car_3.png", 1)
        road.append(car)
        x += 128
    x = 60
    for _ in range(2):
        car = Car(x, ys[3], "data/car_4.png")
        road.append(car)
        x += 128
    x = 80
    for _ in range(2):
        car = Car(x, ys[4], "data/car_5.png", 1)
        road.append(car)
        x += 176

    return road

def create_river():
    "Create the Turtle and Log instances"
    river = []
    ys = [120, 160, 200, 240, 280]
    x = 0
    for _ in range(4):
        turtle = Turtle(x, ys[4], "data/turtle_3_full.png", 1)
        river.append(turtle)
        x += 128
    x = 20
    for _ in range(3):
        log = Log(x, ys[3], "data/tree_small.png")
        river.append(log)
        x += 192
    x = 40
    for _ in range(2):
        log = Log(x, ys[2], "data/tree_big.png")
        river.append(log)
        x += 256
    x = 60
    for _ in range(4):
        turtle = Turtle(x, ys[1], "data/turtle_2_full.png", 1)
        river.append(turtle)
        x += 112
    x = 80
    for _ in range(3):
        log = Log(x, ys[0], "data/tree_medium.png")
        river.append(log)
        x += 176

    return river

def main():

    start_screen()

    # Basic setup.
    clock = pygame.time.Clock()
    background = pygame.image.load("data/background.png")
    frog, enemy = Frog(), StaticObstacle()
    road, river = create_road(), create_river()

    level = 0

    while True:
        # Poll for events and apply actions accordingly.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_SPACE:
                    frog.death()
#                     level += 1
                    print frog.x, frog.y, frog.lives
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    frog.left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    frog.right()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    frog.forward()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    frog.back()

        # Draw the background image.
        window.blit(background, (0, 0))

        # Update all our objects and images.
        for i in road + river:
            i.update()
        # Update the frog last so that he is on top of other objects.
        frog.update()

        # If we're out of lives, invoke the game over screen.
        frog.update_lives()
        if not frog.lives:
            game_over()

        # Set the FPS to 30. To implement a rudimentary difficulty system, we
        # increment the FPS by 10 per level to speed up the game.
        clock.tick(30 + (level * 10))

        # Everything is drawn. Now we refresh the display to reflect the
        # changes.
        pygame.display.flip()


if __name__ == '__main__':
    # Initialize Pygame, the screen/window and some globals.
    pygame.init()
    window = pygame.display.set_mode((480, 600), 0, 32)
    game_zone = window.get_rect()
    main()
