import pygame
import os

# Directory of this file (utils folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up from utils → scripts → project
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")


def load_image(filename, convert_alpha=True):
    path = os.path.join(IMAGES_DIR, filename)
    image = pygame.image.load(path)

    if convert_alpha:
        return image.convert_alpha()
    return image.convert()


def load_sound(filename):
    path = os.path.join(SOUNDS_DIR, filename)
    return pygame.mixer.Sound(path)


def load_music(filename):
    path = os.path.join(MUSIC_DIR, filename)
    pygame.mixer.music.load(path)