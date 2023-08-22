import pygame
import os

def init():
    global WIDTH, HEIGHT, WINDOW, FPS, BACKGROUND, DIVIDER_WIDTH, DIVIDER, BLACK, PLAYER_WIDTH  
    global PLAYER_HEIGHT, PLAYER_VELOCITY, DODGEBALL_SIZE, DODGEBALL_VELOCITY, DODGEBALL_NUMBERS
    global SPAWN_TOP_PADDING, SPAWN_SIDE_PADDING, SPAWN_BETWEEN_BALL_PADDING

    # window configurations
    WIDTH, HEIGHT = 900, 500
    WINDOW =  pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodgeball")

    FPS = 60

    # background and divider configurations
    BACKGROUND = pygame.image.load(os.path.join('Assets', 'grass_background.jpg')).convert()
    DIVIDER_WIDTH = 10
    DIVIDER = pygame.Rect(WIDTH//2 - DIVIDER_WIDTH, 0, 10, HEIGHT)

    # rgb colors
    BLACK = (0, 0, 0)

    # player configurations
    PLAYER_WIDTH, PLAYER_HEIGHT = 45, 70
    PLAYER_VELOCITY = 4

    # dodgeball configurations
    DODGEBALL_SIZE = 15
    DODGEBALL_VELOCITY = 8
    DODGEBALL_NUMBERS = 3
    SPAWN_TOP_PADDING, SPAWN_SIDE_PADDING = 50, 10
    SPAWN_BETWEEN_BALL_PADDING = 5