import pygame
import os

def init():
    global WIDTH, HEIGHT, WINDOW, FPS, BACKGROUND, DIVIDER_WIDTH, DIVIDER, BLACK, PLAYER_WIDTH  
    global PLAYER_HEIGHT, PLAYER_VELOCITY 

    # window configuration
    WIDTH, HEIGHT = 900, 500
    WINDOW =  pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodgeball")

    FPS = 60

    # background and divider configuration
    BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join
                            ('Assets', 'grassBackground.png')), (WIDTH, HEIGHT))
    DIVIDER_WIDTH = 10
    DIVIDER = pygame.Rect(WIDTH//2 - DIVIDER_WIDTH, 0, 10, HEIGHT)

    # rgb colors
    BLACK = (0, 0, 0)

    # player configuration
    PLAYER_WIDTH, PLAYER_HEIGHT = 45, 70
    PLAYER_VELOCITY = 4