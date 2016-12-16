#! /usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
from random import randrange

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)

screen = pygame.display.set_mode((956, 560), 0, 32)

background_filename = 'img/background.png'
background = pygame.image.load(background_filename).convert()

ship = {
    'surface': pygame.image.load('img/spacefighter.png').convert_alpha(),
    'position': [450, 500],
    'speed': {
        'x': 0,
        'y': 0
    }
}

exploded_ship = {
    'surface': pygame.image.load('img/exploded_spacefighter.png').convert_alpha(),
    'position': [],
    'speed': {
        'x': 0,
        'y': 0
    },
    'rect': Rect(0, 0, 48, 48)
}

firing_ship = {
    'surface': pygame.image.load('img/shooting_spacefighter.png').convert_alpha(),
    'position': [],
    'speed': {
        'x': 0,
        'y': 0
    },
    'rect': Rect(0, 0, 48, 48)
}

explosion_sound = pygame.mixer.Sound('audio/boom.wav')
explosion_played = False
pygame.display.set_caption('Space Fighter')

clock = pygame.time.Clock()


def create_asteroid():
    return {
        'surface': pygame.image.load('img/asteroid.png').convert_alpha(),
        'position': [randrange(892), -64],
        'speed': randrange(1, 12)
    }

ticks_to_asteroid = 60
asteroids = []


def move_asteroids():
    for asteroid in asteroids:
        asteroid['position'][1] += asteroid['speed']


def remove_used_asteroids():
    for asteroid in asteroids:
        if asteroid['position'][1] > 560:
            asteroids.remove(asteroid)


def get_rect(obj):
    return Rect(obj['position'][0],
                obj['position'][1],
                obj['surface'].get_width(),
                obj['surface'].get_height())


def ship_collided():
    ship_rect = get_rect(ship)
    for asteroid in asteroids:
        if ship_rect.colliderect(get_rect(asteroid)):
            return True
    return False


# http://codereview.stackexchange.com/questions/117875/space-shooter-made-using-pygame

collided = False
collision_animation_counter = 0

while True:

    if not ticks_to_asteroid:
        ticks_to_asteroid = 60
        asteroids.append(create_asteroid())
    else:
        ticks_to_asteroid -= 1

    if ship['speed']['x'] > 0:
        ship['speed']['x'] -= 1
    elif ship['speed']['x'] < 0:
        ship['speed']['x'] += 1

    if ship['speed']['y'] > 0:
        ship['speed']['y'] -= 1
    elif ship['speed']['y'] < 0:
        ship['speed']['y'] += 1

    # ship['speed'] = {
    #     'x': 0,
    #     'y': 0
    # }

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_UP]:
        ship['speed']['y'] = -12
    elif pressed_keys[K_DOWN]:
        ship['speed']['y'] = 12

    if pressed_keys[K_LEFT]:
        ship['speed']['x'] = -12
    elif pressed_keys[K_RIGHT]:
        ship['speed']['x'] = 12

    screen.blit(background, (0, 0))

    move_asteroids()

    for asteroid in asteroids:
        screen.blit(asteroid['surface'], asteroid['position'])

    if not collided:
        collided = ship_collided()
        ship['position'][0] += ship['speed']['x']
        ship['position'][1] += ship['speed']['y']

        screen.blit(ship['surface'], ship['position'])
    else:
        if not explosion_played:
            explosion_played = True
            explosion_sound.play()
            ship['position'][0] += ship['speed']['x']
            ship['position'][1] += ship['speed']['y']

            screen.blit(ship['surface'], ship['position'])
        elif collision_animation_counter == 3:
            text = game_font.render('GAME OVER', 1, (255, 0, 0))
            screen.blit(text, (335, 250))
        else:
            exploded_ship['rect'].x = collision_animation_counter * 48
            exploded_ship['position'] = ship['position']
            screen.blit(exploded_ship['surface'], exploded_ship['position'],
                        exploded_ship['rect'])
            collision_animation_counter += 1

    pygame.display.update()
    time_passed = clock.tick(30)

    remove_used_asteroids()