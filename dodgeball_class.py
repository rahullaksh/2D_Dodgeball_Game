import config
import pygame
import os

class Dodgeball:
    def __init__(self, direction, number):
        self.direction = direction
        self.__number = number

        # valid initialization checks
        if direction == 'RIGHT' or direction == 'LEFT': pass
        else: raise TypeError("Invalid 'direction' during Dodgeball object instantiation")
        if self.__number < 0 or self.__number > config.DODGEBALL_NUMBERS:
            raise TypeError("Invalid 'number' during Dodgeball object instantiation")
        

        # spawn location and spacing
        if direction == 'RIGHT':
            SPAWN_X = config.WIDTH - config.SPAWN_SIDE_PADDING - config.DODGEBALL_SIZE
        else:
            SPAWN_X = config.SPAWN_SIDE_PADDING
        SPAWN_Y = config.SPAWN_TOP_PADDING + config.DODGEBALL_SIZE * number
        if self.__number > 0: 
            SPAWN_Y = SPAWN_Y + config.SPAWN_BETWEEN_BALL_PADDING * number
        self.__spawn = (SPAWN_X, SPAWN_Y)

        # load image and hitbox
        DODGEBALL_IMAGE = pygame.image.load(os.path.join('Assets', 'red_dodgeball.png'))
        self.ball = pygame.transform.scale(DODGEBALL_IMAGE, (config.DODGEBALL_SIZE, config.DODGEBALL_SIZE))
        self.hitbox = pygame.Rect(self.__spawn[0], self.__spawn[1], config.DODGEBALL_SIZE, config.DODGEBALL_SIZE)
        
