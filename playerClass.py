import pygame
import config
from dodgeballClass import Dodgeball
from animationClass import Animation

class Player:
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
    HIT_FRAME_COORDINATES = [((286, 125), (321, 173)), 
                             ((321, 125), (356, 173)), 
                             ((356, 125), (391,173)),
                             ((286, 125), (321, 173)), 
                             ((321, 125), (356, 173)), 
                             ((356, 125), (391,173))]
     
    ACTIONS = {'idle': Animation(IDLE_FRAME_COORDINATES, 6), 
               'run': Animation(RUN_FRAME_COORDINATES, 6), 
               'throw': Animation(THROW_FRAME_COORDINATES, 3),
               'hit': Animation(HIT_FRAME_COORDINATES, 6)}

    def __init__(self, player_section):
        # attributes: player_selection, dodgeballs, player, hitbox, balls
        self.player_section = player_section
        self.dodgeball = None       # dodgeball id that the player is holding
        self.ball_list = []
        self.direction = None
        self.lives = 3

        self.frame = 0
        self.last_update = 0
        self.current_action = 'idle'
        self.doing_hit = 0

        if player_section == 'RIGHT' or player_section ==  'LEFT':
            pass
        else:
            raise TypeError("Invalid player_section during Player object initialization")
        

        if (player_section == 'RIGHT'):
            self.direction = 'LEFT'
            self.hitbox = pygame.Rect((3 * config.WIDTH)//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT, config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)
            for i in range(config.DODGEBALL_NUMBERS):
                self.ball_list.append(Dodgeball(self.direction, i))

        else:
            self.direction = 'RIGHT'         
            self.hitbox = pygame.Rect(config.WIDTH//4 - config.PLAYER_WIDTH, 
                                      config.HEIGHT//2 - config.PLAYER_HEIGHT,config.PLAYER_WIDTH, 
                                      config.PLAYER_HEIGHT)            
            for i in range(config.DODGEBALL_NUMBERS):
                self.ball_list.append(Dodgeball(self.direction, i))


    def _Move_Left(self):
        self.hitbox.x -= config.PLAYER_VELOCITY
        self.direction = 'LEFT'
        self.current_action = 'run'
    def _Move_Right(self):
        self.hitbox.x += config.PLAYER_VELOCITY
        self.direction = 'RIGHT'
        self.current_action = 'run'
    def _Move_Up(self):
        self.hitbox.y -= config.PLAYER_VELOCITY
        self.current_action = 'run'
    def _Move_Down(self):
        self.hitbox.y += config.PLAYER_VELOCITY
        self.current_action = 'run'

    def Get_Ball(self, ball_id):
        return self.ball_list[ball_id]

    def _Handle_Movement(self, keys_pressed):
        if not any(keys_pressed) and self.current_action != 'throw' and self.current_action != 'hit':
            self.current_action = 'idle'
        elif self.player_section == 'LEFT' and self.current_action != 'throw' and self.current_action != 'hit':
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
        elif self.player_section == 'RIGHT' and self.current_action != 'throw' and self.current_action != 'hit':
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
            if self.direction == 'LEFT':
                self.Get_Ball(self.dodgeball).hitbox.x -= 40
                self.Get_Ball(self.dodgeball).direction = 'LEFT'
            else:
                self.Get_Ball(self.dodgeball).hitbox.x += 20
                self.Get_Ball(self.dodgeball).direction = 'RIGHT'

            self.Get_Ball(self.dodgeball).Start_Animation()
            self.current_action = 'throw'
            self.dodgeball = None

    def Draw_Player(self):
        current_time = pygame.time.get_ticks()
        if self.frame >= Player.ACTIONS[self.current_action].Num_Frames(): self.frame = 0

        if self.direction == 'RIGHT': image = Player.ACTIONS[self.current_action].Get_Frame('RIGHT', self.frame)
        else: image = Player.ACTIONS[self.current_action].Get_Frame('LEFT', self.frame)
        if self.current_action == 'hit': 
            if self.frame % 2 == 0: image.set_alpha(150)
            else: image.set_alpha(250)

        config.WINDOW.blit(image, (self.hitbox.x, self.hitbox.y))

        if self.current_action != 'hit':
            speed = 100
            if current_time - self.last_update >= speed:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= Player.ACTIONS[self.current_action].Num_Frames():
                    if self.current_action == 'throw': self.current_action = 'idle'
                    self.frame = 0
        else:
            speed = 300
            if current_time - self.last_update >= speed:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= Player.ACTIONS[self.current_action].Num_Frames():
                    self.doing_hit += 1
                    self.frame = 0
                    if self.doing_hit >= 2:
                        self.current_action = 'idle'
                        image.set_alpha(250)

def Initialize_Player_Animations():
    Player.ACTIONS['idle'].Set_Frames('RIGHT', Extract_Animation('idle'))
    Player.ACTIONS['run'].Set_Frames('RIGHT', Extract_Animation('run'))
    Player.ACTIONS['throw'].Set_Frames('RIGHT', Extract_Animation('throw'))
    Player.ACTIONS['hit'].Set_Frames('RIGHT', Extract_Animation('hit'))

    rotate_left = lambda frame: pygame.transform.flip(frame, True, False)
    for action in Player.ACTIONS:
        for j in range(Player.ACTIONS[action].Num_Frames()):
            Player.ACTIONS[action].Append_Frame('LEFT', rotate_left(Player.ACTIONS[action].Get_Frame('RIGHT', j)))

def Extract_Animation(action):
    temp_animation_list = []

    for i in range(Player.ACTIONS[action].Num_Frames()):
        start_x = Player.ACTIONS[action].Get_Start_Frame_Point(i, 'x')
        start_y = Player.ACTIONS[action].Get_Start_Frame_Point(i, 'y')
        finish_x = Player.ACTIONS[action].Get_End_Frame_Point(i, 'x')
        finish_y = Player.ACTIONS[action].Get_End_Frame_Point(i, 'y')

        image = pygame.Surface((config.PLAYER_ORIGINAL_WIDTH, config.PLAYER_ORIGINAL_HEIGHT)).convert()
        image.fill((138,180,18))
        image.blit(config.PLAYER_SPRITESHEET, (0, 0), (start_x, start_y, finish_x, finish_y))
        image = pygame.transform.scale(image, (config.PLAYER_WIDTH, config.PLAYER_HEIGHT))
        image.set_colorkey((138,180,18))
        temp_animation_list.append(image)

    return temp_animation_list

def Disable_Movement(hitbox):
    hitbox.x = hitbox.x
    hitbox.y = hitbox.y