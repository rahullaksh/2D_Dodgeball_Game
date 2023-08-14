import pygame
import os
import config

class Player:

    def __init__(self, player_section = 'RIGHT' or 'LEFT'):
        self.player_section = player_section

        if (player_section == 'RIGHT'):
            RIGHT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'rightPlayer.png'))
            self.player = pygame.transform.scale(RIGHT_PLAYER_IMAGE, (config.PLAYER_WIDTH, config.PLAYER_HEIGHT))

            self.hitbox = pygame.Rect((3 * config.WIDTH)//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT, config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)
        else:
            LEFT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'rightPlayer.png'))
            self.player = pygame.transform.flip(pygame.transform.scale(LEFT_PLAYER_IMAGE, 
                                                (config.PLAYER_WIDTH, config.PLAYER_HEIGHT)), True, False)
            
            self.hitbox = pygame.Rect(config.WIDTH//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT,config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)