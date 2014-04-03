#!/usr/bin/env python2
"""
    Created on 1 Apr 2014

    @author: Max Demian

    Todo:
    * Home Zone (+img_safe)
    * Timer
    * Animations (Frog + Turtles)
    * Class that creates and holds all the objects as sprite groups
    * Handle sprites better (separation, SpriteGroups, ...)
    * Sounds & Music
    * Score and Highscores
"""

import pygame
import sys
from random import choice, randrange


class StaticObstacle(pygame.sprite.Sprite):

    def __init__(self):
        super(StaticObstacle, self).__init__()
        self.spawns = [420, 320, 220, 120, 20]
        self.duration = randrange(5, 11)
        self.imgs = ["data/croc.png", "data/fly.png"]
        self.img = pygame.image.load(choice(self.imgs))
        self.rect = self.img.get_rect()
        self.rect.x = choice(self.spawns)
        self.rect.y = 80



class MovingObstacle(pygame.sprite.Sprite):
    "Base class for all moving obstacles"
    def __init__(self, x, y, img, direction):
        super(MovingObstacle, self).__init__()
        self.speed = 2
        self.go_left = direction
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        "Moves and then draws the obstacle"
        # Adjust the position of the obstacle.
        if self.go_left:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        # Reset the object if it moves out of screen.
        if isinstance(self, Car):
            if self.rect.x > 480:
                self.rect.x = -40
            elif self.rect.x < -40:
                self.rect.x = 480
        else:
            # To accomodate the big logs and introduce gaps, we use -180 here.
            if self.rect.x > 480:
                self.rect.x = -180
            elif self.rect.x < -180:
                self.rect.x = 480

        # Update the rectangle position.
        # And finally draw it.
        window.blit(self.img, (self.rect.x, self.rect.y))


class Car(MovingObstacle):

    def __init__(self, x, y, img, direction=0):
        super(Car, self).__init__(x, y, img, direction)


class Turtle(MovingObstacle):

    def __init__(self, x, y, img, direction=0):
        super(Turtle, self).__init__(x, y, img, direction)


class Log(MovingObstacle):

    def __init__(self, x, y, img, direction=0):
        super(Log, self).__init__(x, y, img, direction)


class Frog(pygame.sprite.Sprite):

    def __init__(self):
        super(Frog, self).__init__()
        self.lives = 4
        self.img_f = pygame.image.load("data/frog.png")
        self.img_b = pygame.image.load("data/frog_back.png")
        self.img_l = pygame.image.load("data/frog_left.png")
        self.img_r = pygame.image.load("data/frog_right.png")
        self.img_safe = pygame.image.load("data/frog_safe.png")
        self.img_life = pygame.image.load("data/lives.png")
        self.img_death = pygame.image.load("data/frog_death_3.png")
        self.img = self.img_f
        self.rect = self.img.get_rect()
        self.rect.x = 220
        self.rect.y = 560
        self.startpos = (self.rect.x, self.rect.y)

    def update(self):
        self.move()
        self.display_lives()
        window.blit(self.img, (self.rect.x, self.rect.y))

    def move(self):
        self.rect.move(self.rect.x, self.rect.y)
        # Ensure the player stays within the playable zone.
        self.rect.clamp_ip(pygame.Rect((0, 80), (480, 520)))

    def left(self):
        self.img = self.img_l
        self.rect.x -= 20

    def right(self):
        self.img = self.img_r
        self.rect.x += 20

    def forward(self):
        self.img = self.img_f
        self.rect.y -= 40

    def back(self):
        self.img = self.img_b
        self.rect.y += 40

    def display_lives(self):
        "Draw the life bar"
        x, y = 0, 40
        for _ in range(self.lives):
            window.blit(self.img_life, (x, y))
            x += 20

    def death(self):
        "Update lives, trigger visual clues and reset frog position to default"
        # TODO: Update lives display as soon as death occurs.
        self.lives -= 1
        self.img = self.img_death
        self.update()
        pygame.display.flip()
        pygame.time.wait(500)
        self.rect.x, self.rect.y = self.startpos
        self.img = self.img_f


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


def create_floatables():
    "Create the Turtle and Log instances"
    floatables = pygame.sprite.Group()
    ys = [128, 160, 208, 248, 280]
    x = 0
    for _ in range(4):
        turtle = Turtle(x, ys[4], "data/turtle_3_full.png", 1)
        floatables.add(turtle)
        x += 128
    x = 20
    for _ in range(3):
        log = Log(x, ys[3], "data/log_small.png")
        floatables.add(log)
        x += 192
    x = 40
    for _ in range(2):
        log = Log(x, ys[2], "data/log_big.png")
        floatables.add(log)
        x += 256
    x = 60
    for _ in range(4):
        turtle = Turtle(x, ys[1], "data/turtle_2_full.png", 1)
        floatables.add(turtle)
        x += 112
    x = 80
    for _ in range(3):
        log = Log(x, ys[0], "data/log_medium.png")
        floatables.add(log)
        x += 176

    return floatables


def create_hostiles():
    "Create the obstacles that trigger death on collision"
    hostiles = pygame.sprite.Group()
    ys = [520, 480, 440, 400, 360]
    x = randrange(200)
    for _ in range(3):
        car = Car(x, ys[0], "data/car_1.png", 1)
        hostiles.add(car)
        x += 144
    x = randrange(200)
    for _ in range(3):
        car = Car(x, ys[1], "data/car_2.png")
        hostiles.add(car)
        x += 128
    x = randrange(200)
    for _ in range(3):
        car = Car(x, ys[2], "data/car_3.png", 1)
        hostiles.add(car)
        x += 128
    x = randrange(200)
    for _ in range(2):
        car = Car(x, ys[3], "data/car_4.png")
        hostiles.add(car)
        x += 128
    x = randrange(200)
    for _ in range(2):
        car = Car(x, ys[4], "data/car_5.png", 1)
        hostiles.add(car)
        x += 176

    return hostiles


def create_homezones():
    "Create the 5 safety zones at the top of the map"
    xs = [420, 320, 220, 120, 20]
    y = 80


def main():

    start_screen()

    # Basic setup.
    clock = pygame.time.Clock()
    background = pygame.image.load("data/background.png")
    top_ground = pygame.image.load("data/top_ground.png")
    frog, enemy = Frog(), StaticObstacle()
    # Sprite groups
    hostiles, floatables = create_hostiles(), create_floatables()
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
#                     level += 1
                    print frog.rect.x, frog.rect.y
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

        # Create the death-zone at the top of the map.
        deathzone = pygame.Surface((480, 56), pygame.SRCALPHA)
        deathzone.fill((255, 255, 255, 128))
        window.blit(deathzone, (0, 62))


        # First, draw the floating obstacles.
        for i in floatables:
            i.update()
        # Draw the frog so that he appears on top of river objects but beneath
        # hostiles.
        frog.update()

        for i in hostiles:
            i.update()

        # Handle collision.

        for i in pygame.sprite.spritecollide(frog, hostiles, False):
            pass
#             frog.death()
        for i in pygame.sprite.spritecollide(frog, floatables, False):
#             if i.go_left:
#                 frog.rect.x -= i.speed
#             else:
#                 frog.rect.x += i.speed
            pass

        # If we're out of lives, invoke the game over screen.
        if not frog.lives:
            game_over()

        # Set the FPS to 30. To implement a rudimentary difficulty system, we
        # increment the FPS by 10 per level to speed up the game.
        clock.tick(30 + (level * 10))

        # Everything is drawn. Now we refresh the display to reflect the
        # changes.
        pygame.display.update()


if __name__ == '__main__':
    # Initialize Pygame, the screen/window and some globals.
    pygame.init()
    window = pygame.display.set_mode((480, 600), 0, 32)
    main()
