import config
import pygame
import os

class Dodgeball:
    def __init__(self, direction, number):
        self.direction = direction
        self.__id = number
        self.traveling = False
        self.stick = False

        self.frame = 0
        self.animation_list = []
        self.last_update = -1

        # valid initialization checks
        if direction == 'RIGHT' or direction == 'LEFT': pass
        else: raise TypeError("Invalid 'direction' during Dodgeball object instantiation")
        if self.__id < 0 or self.__id > config.DODGEBALL_NUMBERS:
            raise TypeError("Invalid 'number' during Dodgeball object instantiation")
        

        # spawn location and spacing
        if direction == 'RIGHT':
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
            self.animation_list.append(temp_ball)

    def _Stick(self, player):
        # makes ball stick to player
        if self.stick:
            if player.player_section == 'RIGHT':
                player.Get_Ball(self.__id).hitbox.x = player.hitbox.x - 8
                player.Get_Ball(self.__id).hitbox.y = (player.hitbox.y + config.PLAYER_HEIGHT // 2 - 10)
            else:
                player.Get_Ball(self.__id).hitbox.x = (player.hitbox.x + config.PLAYER_WIDTH - 10)
                player.Get_Ball(self.__id).hitbox.y = (player.hitbox.y + config.PLAYER_HEIGHT // 2)

    def __Delete(self):
        self.hitbox.x = self.__spawn[0]
        self.hitbox.y = self.__spawn[1]
        self.traveling = False
        self.stick = False
        return
    
    def _Get_Id(self):
        return self.__id
    
    def Start_Animation(self):
        self.last_update = pygame.time.get_ticks()

    def _Travel(self, player):
        if player.player_section == 'LEFT':
            self.hitbox.x += config.DODGEBALL_VELOCITY
        else:
            self.hitbox.x -= config.DODGEBALL_VELOCITY 
        
        if self.hitbox.x > config.WIDTH - config.DODGEBALL_SIZE or self.hitbox.x < 0:
            self.__Delete()
        else:
            # cycle through animation_list for traveling animation
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= config.BALL_ANIMATION_SPEED:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= 4:
                    self.frame = 0

    def Display_Frame(self):
        if self.traveling: return self.animation_list[self.frame]
        else: return self.animation_list[0]
            