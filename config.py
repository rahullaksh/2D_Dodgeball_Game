import pygame
import os

def init():
    global WIDTH, HEIGHT, WINDOW, FPS, BACKGROUND, DIVIDER_WIDTH, DIVIDER, BLACK, PLAYER_WIDTH  
    global PLAYER_HEIGHT, PLAYER_VELOCITY, DODGEBALL_SIZE, DODGEBALL_VELOCITY, DODGEBALL_NUMBERS
    global SPAWN_TOP_PADDING, SPAWN_SIDE_PADDING, SPAWN_BETWEEN_BALL_PADDING, BALL_ANIMATION_SPEED
    global PLAYER_SPRITESHEET, PLAYER_SIZE_SCALE, PLAYER_ORIGINAL_WIDTH 
    global PLAYER_ORIGINAL_HEIGHT, IDLE_FRAME_COORDINATES, RUN_FRAME_COORDINATES, THROW_FRAME_COORDINATES
    global LEFT_PLAYER_HIT, RIGHT_PLAYER_HIT, LIVES_FONT, WIN_FONT, END_GAME

    # window configurations
    WIDTH, HEIGHT = 900, 500
    WINDOW =  pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodgeball")

    LIVES_FONT = pygame.font.SysFont('terminal', 35)
    WIN_FONT = pygame.font.SysFont('comicsans', 100)
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
    PLAYER_ORIGINAL_WIDTH, PLAYER_ORIGINAL_HEIGHT = 29, 51
    PLAYER_SIZE_SCALE = 1.5
    PLAYER_WIDTH = PLAYER_ORIGINAL_WIDTH * PLAYER_SIZE_SCALE
    PLAYER_HEIGHT = PLAYER_ORIGINAL_HEIGHT * PLAYER_SIZE_SCALE
    PLAYER_VELOCITY = 4
    PLAYER_SPRITESHEET = pygame.image.load(os.path.join('Assets', 'character_spritesheet.png')).convert_alpha()

    # dodgeball configurations
    DODGEBALL_SIZE = 20
    DODGEBALL_VELOCITY = 8
    DODGEBALL_NUMBERS = 3
    BALL_ANIMATION_SPEED = 50
    SPAWN_TOP_PADDING, SPAWN_SIDE_PADDING = 50, 10
    SPAWN_BETWEEN_BALL_PADDING = 5

    # animation configurations
    IDLE_FRAME_COORDINATES = [((0, 0), (30, 50)), 
                              ((33, 0), (62, 50)), 
                              ((68, 0), (100, 50)),
                              ((103, 0), (134, 50)),
                              ((137, 0), (168, 50)),
                              ((171, 0), (200, 50))]
    RUN_FRAME_COORDINATES = [((206, 61), (235, 113)),
                             ((235, 61), (264, 113)),
                             ((264, 61), (304, 113)),
                             ((307, 61), (338, 113)),
                             ((340, 61), (372, 113)),
                             ((372, 61), (405, 113))]
    THROW_FRAME_COORDINATES = [((148, 121), (184, 171)),
                               ((188, 121), (222, 171)),
                               ((223, 121), (262, 171))]
    
    LEFT_PLAYER_HIT = pygame.USEREVENT + 1
    RIGHT_PLAYER_HIT = pygame.USEREVENT + 2
    END_GAME = pygame.USEREVENT + 3