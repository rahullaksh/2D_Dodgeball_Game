import config
import pygame
import os

class Dodgeball:
    def __init__(self, direction, number):
        self.direction = direction
        self.__number = number
        self.safe = True
        self.traveling = False

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

    def _Stick(self, player, ball_id):
        # makes ball stick to player
        if player.player_section == 'RIGHT' and not self.traveling:
            player.dodgeballs[ball_id].hitbox.x = player.hitbox.x + 10
            player.dodgeballs[ball_id].hitbox.y = (player.hitbox.y + config.PLAYER_HEIGHT // 2)
        elif not self.traveling:
            player.dodgeballs[ball_id].hitbox.x = (player.hitbox.x + config.PLAYER_WIDTH - 10)
            player.dodgeballs[ball_id].hitbox.y = (player.hitbox.y + config.PLAYER_HEIGHT // 2)

    def __Delete(self):
        self.hitbox.x = self.__spawn[0]
        self.hitbox.y = self.__spawn[1]
        self.traveling = False

    def _Travel(self, player):
        self.traveling = True
        if player.player_section == 'LEFT':
            self.hitbox.x += config.DODGEBALL_VELOCITY
        else:
            self.hitbox.x -= config.DODGEBALL_VELOCITY 
        
        if self.hitbox.x > config.WIDTH - config.DODGEBALL_SIZE or self.hitbox.x < 0:
            self.__Delete()
