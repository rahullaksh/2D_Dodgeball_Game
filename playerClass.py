import pygame
import os
import config

class Player:

    def __init__(self, player_section = 'RIGHT' or 'LEFT'):
        self.player_section = player_section
        self.balls = 3

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
    
    def Move_Left(self):
        self.hitbox.x -= config.PLAYER_VELOCITY
    def Move_Right(self):
        self.hitbox.x += config.PLAYER_VELOCITY
    def Move_Up(self):
        self.hitbox.y -= config.PLAYER_VELOCITY
    def Move_Down(self):
        self.hitbox.y += config.PLAYER_VELOCITY

    def Handle_Movement(self, keys_pressed):
        if self.player_section == 'LEFT':
            if keys_pressed[pygame.K_w] and self.hitbox.y - config.PLAYER_VELOCITY > 0:
                self.Move_Up()
            if keys_pressed[pygame.K_s] and self.hitbox.y + config.PLAYER_HEIGHT + \
                config.PLAYER_VELOCITY < config.HEIGHT:
                self.Move_Down()
            if keys_pressed[pygame.K_a] and self.hitbox.x - config.PLAYER_VELOCITY > 0:
                self.Move_Left()
            if keys_pressed[pygame.K_d] and self.hitbox.x + config.PLAYER_WIDTH + \
                config.PLAYER_VELOCITY < config.WIDTH // 2 - config.DIVIDER_WIDTH:
                self.Move_Right()
        else:
            if keys_pressed[pygame.K_UP] and self.hitbox.y - config.PLAYER_VELOCITY > 0:
                self.Move_Up()
            if keys_pressed[pygame.K_DOWN] and (self.hitbox.y + config.PLAYER_HEIGHT +
                config.PLAYER_VELOCITY < config.HEIGHT):
                self.Move_Down()
            if keys_pressed[pygame.K_LEFT] and (self.hitbox.x - config.PLAYER_VELOCITY > 
                config.WIDTH // 2):
                self.Move_Left()
            if keys_pressed[pygame.K_RIGHT] and (self.hitbox.x + config.PLAYER_WIDTH +
                config.PLAYER_VELOCITY < config.WIDTH):
                self.Move_Right()

    def Throw(self):
        self.balls -= 1