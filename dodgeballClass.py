import config
import pygame
import os
from animationClass import Animation

class Dodgeball:
    ANIMATION = Animation([(0, 0)], 4)

    def __init__(self, direction, number):
        self.direction = direction
        self.__id = number
        self.traveling = False
        self.stick = False

        self.frame = 0
        self.last_update = 0

        # valid initialization checks
        if direction == 'RIGHT' or direction == 'LEFT': pass
        else: raise TypeError("Invalid 'direction' during Dodgeball object instantiation")
        if self.__id < 0 or self.__id > config.DODGEBALL_NUMBERS:
            raise TypeError("Invalid 'number' during Dodgeball object instantiation")
        

        # spawn location and spacing
        if self.direction == 'LEFT':
            SPAWN_X = config.WIDTH - config.SPAWN_SIDE_PADDING - config.DODGEBALL_SIZE
        else:
            SPAWN_X = config.SPAWN_SIDE_PADDING
        SPAWN_Y = config.SPAWN_TOP_PADDING + config.DODGEBALL_SIZE * number
        if self.__id > 0: 
            SPAWN_Y = SPAWN_Y + config.SPAWN_BETWEEN_BALL_PADDING * number
        self.__spawn = (SPAWN_X, SPAWN_Y)

        # load image and hitbox
        DODGEBALL_IMAGE = pygame.image.load(os.path.join('Assets', 'dodgeball.png')).convert_alpha()
        ball = pygame.transform.scale(DODGEBALL_IMAGE, (config.DODGEBALL_SIZE, config.DODGEBALL_SIZE))
        self.hitbox = pygame.Rect(self.__spawn[0], self.__spawn[1], config.DODGEBALL_SIZE, config.DODGEBALL_SIZE)

        # load animation frames
        for i in range(4):
            temp_ball = pygame.transform.rotate(ball, i * 90)
            Dodgeball.ANIMATION.Append_Frame('RIGHT', temp_ball)

    def _Stick(self, player):
        # makes ball stick to player
        if self.stick:
            if player.direction == 'RIGHT':
                player.Get_Ball(self.__id).hitbox.x = (player.hitbox.x + config.PLAYER_WIDTH - 10)
                player.Get_Ball(self.__id).hitbox.y = (player.hitbox.y + config.PLAYER_HEIGHT // 2)
            elif player.direction == 'LEFT': 
                player.Get_Ball(self.__id).hitbox.x = player.hitbox.x - 8
                player.Get_Ball(self.__id).hitbox.y = (player.hitbox.y + config.PLAYER_HEIGHT // 2 - 10)

    def _Delete(self):
        self.hitbox.x = self.__spawn[0]
        self.hitbox.y = self.__spawn[1]
        self.traveling = False
        self.stick = False
        return
    
    def _Get_Id(self):
        return self.__id
    
    def Start_Animation(self):
        self.last_update = pygame.time.get_ticks()

    def _Travel(self):
        if self.direction == 'RIGHT':
            self.hitbox.x += config.DODGEBALL_VELOCITY
        else:
            self.hitbox.x -= config.DODGEBALL_VELOCITY 
        
        if self.hitbox.x > config.WIDTH - config.DODGEBALL_SIZE or self.hitbox.x < 0:
            self._Delete()
        else:
            # cycle through animation_list for traveling animation
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= config.BALL_ANIMATION_SPEED:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= 4:
                    self.frame = 0

    def Display_Frame(self):
        if self.traveling: return Dodgeball.ANIMATION.Get_Frame('RIGHT', self.frame)
        else: return Dodgeball.ANIMATION.Get_Frame('RIGHT', 0)
            
    def Check_Hit(self, player):
        if self.hitbox.colliderect(player.hitbox):
            if player.player_section == 'RIGHT':
                pygame.event.post(pygame.event.Event(config.RIGHT_PLAYER_HIT))
                self._Delete()
            elif player.player_section == 'LEFT':
                pygame.event.post(pygame.event.Event(config.LEFT_PLAYER_HIT))
                self._Delete()