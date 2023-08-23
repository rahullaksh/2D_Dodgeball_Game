import pygame
import os
import config
from dodgeballClass import Dodgeball

class Player:
    animations = { 'idle'  : {'animation_start_coordinates' : (0, 0), 'right_animation': [], 
                              'left_animation' : [], 'frames' : 6},
                   'run'   : {'animation_start_coordinates' : (205, 61), 'right_animation': [], 
                              'left_animation' : [], 'frames' : 6},
                   'throw' : {'animation_start_coordinates' : (287, 126), 'right_animation': [], 
                              'left_animation' : [], 'frames' : 3} }
    
    def __init__(self, player_section):
        # attributes: player_selection, dodgeballs, player, hitbox, balls
        self.player_section = player_section
        self.dodgeball = None       # dodgeball id that the player is holding
        self.ball_list = []
        self.direction = None

        self.frame = 0
        self.last_update = 0
        self.current_action = 'idle'

        if player_section == 'RIGHT' or player_section ==  'LEFT':
            pass
        else:
            raise TypeError("Invalid player_section during Player object initialization")
        

        if (player_section == 'RIGHT'):
            self.direction = 'LEFT'
            RIGHT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'right_player.png')).convert_alpha()
            RIGHT_PLAYER_IMAGE.set_colorkey((255, 255, 255))
            self.player = pygame.transform.scale(RIGHT_PLAYER_IMAGE, (config.PLAYER_WIDTH, config.PLAYER_HEIGHT))

            self.hitbox = pygame.Rect((3 * config.WIDTH)//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT, config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)
            
            for i in range(config.DODGEBALL_NUMBERS):
                self.ball_list.append(Dodgeball('RIGHT', i))

        else:
            self.direction = 'RIGHT'
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
                config.PLAYER_VELOCITY < config.WIDTH // 2 - config.DIVIDER_WIDTH + 2:
                self._Move_Right()
        else:
            if keys_pressed[pygame.K_UP] and self.hitbox.y - config.PLAYER_VELOCITY > 0:
                self._Move_Up()
            if keys_pressed[pygame.K_DOWN] and (self.hitbox.y + config.PLAYER_HEIGHT +
                config.PLAYER_VELOCITY < config.HEIGHT):
                self._Move_Down()
            if keys_pressed[pygame.K_LEFT] and (self.hitbox.x - config.PLAYER_VELOCITY > 
                config.WIDTH // 2 - 2):
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

            self.Get_Ball(self.dodgeball).Start_Animation()
            self.dodgeball = None

    def Draw_Player(self):
        current_time = pygame.time.get_ticks()

        if self.current_action == 'idle':
            if self.direction == 'RIGHT': image = self.animations['idle']['right_animation'][self.frame]
            else: image = self.animations['idle']['left_animation'][self.frame]
            config.WINDOW.blit(image, (self.hitbox.x, self.hitbox.y))

            if current_time - self.last_update >= config.PLAYER_ANIMATION_SPEED:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= self.animations['idle']['frames']:
                    self.frame = 0

def Initialize_Player_Animations():
    Player.animations['idle']['right_animation'] = Extract_Animation('idle')
    Player.animations['run']['right_animation'] = Extract_Animation('run')
    Player.animations['throw']['right_animation'] = Extract_Animation('throw')

    rotate_left = lambda frame: pygame.transform.flip(frame, True, False)
    for i in range(Player.animations['idle']['frames']):
        Player.animations['idle']['left_animation'].append(rotate_left(Player.animations['idle']['right_animation'][i]))
    for i in range(Player.animations['run']['frames']):
        Player.animations['run']['left_animation'].append(rotate_left(Player.animations['run']['right_animation'][i]))
    for i in range(Player.animations['throw']['frames']):
        Player.animations['throw']['left_animation'].append(rotate_left(Player.animations['throw']['right_animation'][i]))

def Extract_Animation(animation):
    temp_animation_list = []
    start_coordinates = Player.animations[animation]['animation_start_coordinates']
    original_width, original_height = 29, 51
    start_x, start_y = start_coordinates[0], start_coordinates[1]

    for i in range(Player.animations[animation]['frames']):
        image = pygame.Surface((original_width, original_height)).convert()
        image.fill((138,180,18))
        image.blit(config.PLAYER_SPRITESHEET, (0, 0), (start_x, start_y, start_x + original_width, 
                                                start_y + original_height))
        
        config.PLAYER_WIDTH = original_width * config.PLAYER_SIZE_SCALE
        config.PLAYER_HEIGHT = original_height * config.PLAYER_SIZE_SCALE
        image = pygame.transform.scale(image, (config.PLAYER_WIDTH, config.PLAYER_HEIGHT))
        image.set_colorkey((138,180,18))
        temp_animation_list.append(image)
        if i != 0: start_x = i * (original_width + 6)

    return temp_animation_list