import os
import pygame

prince_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prince')

if os.path.exists(prince_dir):
    os.chdir(prince_dir)

pygame.font.init()
my_font = pygame.font.SysFont("Comic Sans MS", 30)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("audio/background-music.mp3")
pygame.mixer.music.play()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640


# framerate
FPS = 60

# game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 16
screen_scroll = 0
bg_scroll = 0
level = 1

# player action variables
moving_left = False
moving_right = False


# colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
