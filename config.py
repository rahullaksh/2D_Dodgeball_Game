import pygame
import os

def init():
    global WIDTH, HEIGHT, WINDOW, FPS, BACKGROUND, DIVIDER_WIDTH, DIVIDER, BLACK, PLAYER_WIDTH  
    global PLAYER_HEIGHT, PLAYER_VELOCITY, DODGEBALL_SIZE, DODGEBALL_VELOCITY, DODGEBALL_NUMBERS
    global SPAWN_TOP_PADDING, SPAWN_SIDE_PADDING, SPAWN_BETWEEN_BALL_PADDING, BALL_ANIMATION_SPEED

    # window configurations
    WIDTH, HEIGHT = 900, 500
    WINDOW =  pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodgeball")

    FPS = 60

    # background and divider configurations
    BACKGROUND = pygame.image.load(os.path.join('Assets', 'grass_background.jpg')).convert()
    DIVIDER_WIDTH = 10
    divider_image = pygame.image.load(os.path.join('Assets', 'chalk_divider.png')).convert_alpha()
    divider_image = pygame.transform.scale(divider_image, (divider_image.get_width() // 2, 
                                                           divider_image.get_height() // 2))
    DIVIDER = pygame.transform.rotate(divider_image, 90)

    # rgb colors
    BLACK = (0, 0, 0)

    # player configurations
    PLAYER_WIDTH, PLAYER_HEIGHT = 45, 70
    PLAYER_VELOCITY = 4

    # dodgeball configurations
    DODGEBALL_SIZE = 20
    DODGEBALL_VELOCITY = 8
    DODGEBALL_NUMBERS = 3
    BALL_ANIMATION_SPEED = 50
    SPAWN_TOP_PADDING, SPAWN_SIDE_PADDING = 50, 10
    SPAWN_BETWEEN_BALL_PADDING = 5