import pygame
import os
import config
from dodgeballClass import Dodgeball

class Player:
    def __init__(self, player_section):
        # attributes: player_selection, dodgeballs, player, hitbox, balls
        self.player_section = player_section
        self.dodgeball = None       # dodgeball id that the player is holding
        self.ball_list = []


        if player_section == 'RIGHT' or player_section ==  'LEFT':
            pass
        else:
            raise TypeError("Invalid player_section during Player object initialization")
        

        if (player_section == 'RIGHT'):
            RIGHT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'right_player.png')).convert_alpha()
            RIGHT_PLAYER_IMAGE.set_colorkey((255, 255, 255))
            self.player = pygame.transform.scale(RIGHT_PLAYER_IMAGE, (config.PLAYER_WIDTH, config.PLAYER_HEIGHT))

            self.hitbox = pygame.Rect((3 * config.WIDTH)//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT, config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)
            
            for i in range(config.DODGEBALL_NUMBERS):
                self.ball_list.append(Dodgeball('RIGHT', i))

        else:
            LEFT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'right_player.png'))
            self.player = pygame.transform.flip(pygame.transform.scale(LEFT_PLAYER_IMAGE, 
                                                (config.PLAYER_WIDTH, config.PLAYER_HEIGHT)), True, False)
            
            self.hitbox = pygame.Rect(config.WIDTH//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT,config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)
            
            for i in range(config.DODGEBALL_NUMBERS):
                self.ball_list.append(Dodgeball('LEFT', i))
    


    def _Move_Left(self):
        self.hitbox.x -= config.PLAYER_VELOCITY
    def _Move_Right(self):
        self.hitbox.x += config.PLAYER_VELOCITY
    def _Move_Up(self):
        self.hitbox.y -= config.PLAYER_VELOCITY
    def _Move_Down(self):
        self.hitbox.y += config.PLAYER_VELOCITY

    def Get_Ball(self, ball_id):
        return self.ball_list[ball_id]

    def _Handle_Movement(self, keys_pressed):
        if self.player_section == 'LEFT':
            if keys_pressed[pygame.K_w] and self.hitbox.y - config.PLAYER_VELOCITY > 0:
                self._Move_Up()
            if keys_pressed[pygame.K_s] and self.hitbox.y + config.PLAYER_HEIGHT + \
                config.PLAYER_VELOCITY < config.HEIGHT:
                self._Move_Down()
            if keys_pressed[pygame.K_a] and self.hitbox.x - config.PLAYER_VELOCITY > 0:
                self._Move_Left()
            if keys_pressed[pygame.K_d] and self.hitbox.x + config.PLAYER_WIDTH + \
                config.PLAYER_VELOCITY < config.WIDTH // 2 - config.DIVIDER_WIDTH:
                self._Move_Right()
        else:
            if keys_pressed[pygame.K_UP] and self.hitbox.y - config.PLAYER_VELOCITY > 0:
                self._Move_Up()
            if keys_pressed[pygame.K_DOWN] and (self.hitbox.y + config.PLAYER_HEIGHT +
                config.PLAYER_VELOCITY < config.HEIGHT):
                self._Move_Down()
            if keys_pressed[pygame.K_LEFT] and (self.hitbox.x - config.PLAYER_VELOCITY > 
                config.WIDTH // 2):
                self._Move_Left()
            if keys_pressed[pygame.K_RIGHT] and (self.hitbox.x + config.PLAYER_WIDTH +
                config.PLAYER_VELOCITY < config.WIDTH):
                self._Move_Right()
    
    def _Handle_Grab_Ball(self):
        # pick up ball
        if self.dodgeball == None:
            for ball in self.ball_list:
                if self.hitbox.colliderect(ball.hitbox):
                    self.dodgeball = ball._Get_Id()
                    ball.stick = True
                    ball._Stick(self)
                    break
        # holding ball
        else:
            self.Get_Ball(self.dodgeball)._Stick(self)
        return

    def _Throw(self):
        if self.dodgeball != None:
            self.Get_Ball(self.dodgeball).traveling = True
            self.Get_Ball(self.dodgeball).stick = False

            # initial distance to travel to avoid repeat collision after throw 
            if self.player_section == 'RIGHT':
                self.Get_Ball(self.dodgeball).hitbox.x -= 40
            else:
                self.Get_Ball(self.dodgeball).hitbox.x += 20

            self.dodgeball = None