import pygame
import config
import os
from player_class import Player, Initialize_Player_Animations
from button_class import Button
from animation_class import Transition_Animation
pygame.font.init()


def Extract_Key_Icons():
    movement_keys_image = pygame.image.load(os.path.join('Assets', 'movement_keys.png'))
    throw_keys_image = pygame.image.load(os.path.join('Assets', 'space_shift_keys.png'))
    frame_coor = {'a' : ((11, 345),(85, 412)), 's' : ((85, 345), (159, 412)), 'd' : ((159, 345), (233, 412)),
                  'w' : ((89, 268), (163, 335)), 'up' : ((343, 268), (417, 335)), 'down' : ((340, 345), (414, 412)), 
                  'right' : ((414, 345), (488, 412)), 'left': ((266, 345), (340, 412)),
                  'shift' : ((222, 3), (400, 123)), 'space' : ((3, 157), (401, 275))}
    temp_dict = {}

    # extract and store key images
    for key in frame_coor:
        start_x = frame_coor[key][0][0]
        start_y = frame_coor[key][0][1]
        end_x = frame_coor[key][1][0]
        end_y = frame_coor[key][1][1]

        width = end_x - start_x
        height = end_y - start_y
        image = pygame.Surface((width, height)).convert()
        image.fill(config.GREEN)

        # movement keys are same sizes while throw keys are not
        if key == 'shift' or key == 'space': 
            image.blit(throw_keys_image, (0, 0), (start_x, start_y, end_x, end_y))
            image = pygame.transform.scale(image, (width // 3, height // 3))
        else: 
            image.blit(movement_keys_image, (0, 0), (start_x, start_y, end_x, end_y))
            image = pygame.transform.scale(image, (width // 2, height // 2))
        image.set_colorkey(config.GREEN)

        temp_dict[key] = image

    return temp_dict

def Draw_Window():
    # draw background onto window
    draw_x_times = config.WIDTH // config.BACKGROUND.get_width() + 1
    draw_y_times = config.HEIGHT // config.BACKGROUND.get_height() + 1
    for y in range(draw_y_times):
        for x in range(draw_x_times):
            x_position = x * config.BACKGROUND.get_width()
            y_position = y * config.BACKGROUND.get_height()
            config.WINDOW.blit(config.BACKGROUND, (x_position, y_position))

def Draw_Screen(player1, player2, end_game):    
    Draw_Window()

    # draw lives text
    left_player_lives_text = config.LIVES_FONT.render("Lives: " + str(player1.lives), True, (255, 255, 255))
    right_player_lives_text = config.LIVES_FONT.render("Lives: " + str(player2.lives), True, (255, 255, 255))
    config.WINDOW.blit(left_player_lives_text, (5, 10))
    config.WINDOW.blit(right_player_lives_text, (config.WIDTH - right_player_lives_text.get_width() - 5, 10))

    # draw player text
    text = config.PLAYER_NAME_FONT.render("Player 1", True, (255, 0, 0))
    config.WINDOW.blit(text, (200, 10))
    text = config.PLAYER_NAME_FONT.render("Player 2", True, (0, 0, 255))
    config.WINDOW.blit(text, (580, 10))
    
    # draw divider
    extend_divider = config.HEIGHT // config.DIVIDER.get_width() + 1
    for i in range(extend_divider):
        if i == 0:
            config.WINDOW.blit(config.DIVIDER, (config.WIDTH // 2 - config.DIVIDER.get_height() / 2 + 30, 
                                                i * config.DIVIDER.get_width() - 50))
        else:
            config.WINDOW.blit(config.DIVIDER, (config.WIDTH // 2 - config.DIVIDER.get_height() / 2 + 30, 
                                                i * (config.DIVIDER.get_width() - 77)))

    # draw player
    player1.Draw_Player()
    player2.Draw_Player()

    # draw balls
    for i in range(config.DODGEBALL_NUMBERS):
        config.WINDOW.blit(player1.Get_Ball(i).Display_Frame(), (player1.Get_Ball(i).hitbox.x, 
                                                player1.Get_Ball(i).hitbox.y))
        config.WINDOW.blit(player2.Get_Ball(i).Display_Frame(), (player2.Get_Ball(i).hitbox.x, 
                                                player2.Get_Ball(i).hitbox.y))
        
    # draw end game message
    if end_game:
        if player1.lives <= 0: win_message = config.WIN_FONT.render("Player 2 Wins!", True, (config.YELLOW))
        else: win_message = config.WIN_FONT.render("Player 1 Wins!", True, (config.YELLOW))

        pygame.time.delay(1000)
        for i in range(8):
            Draw_Window()
            if i % 2 == 0: win_message.set_alpha(50)
            else: win_message.set_alpha(255)
            config.WINDOW.blit(win_message, ((config.WIDTH - win_message.get_width()) // 2, 
                                                (config.HEIGHT - win_message.get_height()) // 2 - 50))
            pygame.display.update()
            pygame.time.wait(500)

        pygame.time.wait(5000)
        return False    
    
    return True
        
def Draw_Control_Screen(key_icons):
    # controls menu variables
    player_name_font = pygame.font.SysFont('comicsans', 35)
    description_font = pygame.font.SysFont('comicsans', 25)
    divider_image = pygame.image.load(os.path.join('Assets', 'divider.png'))
    divider_image = pygame.transform.rotate(divider_image, 90)

    # draw divider
    config.WINDOW.blit(divider_image, ((config.WIDTH - divider_image.get_width()) // 2, 
                                    (config.HEIGHT - divider_image.get_height()) // 2))
    
    # draw key icons
    i = 0
    leftside_center = 300
    rightside_center = 570
    for key in key_icons:
        if key == 'w': config.WINDOW.blit(key_icons[key], (leftside_center, 150))
        elif key == 's' : config.WINDOW.blit(key_icons[key], 
                                            (leftside_center - 2,  150 + key_icons[key].get_height() + 5))
        elif key == 'a' : config.WINDOW.blit(key_icons[key], 
                                            (leftside_center - key_icons[key].get_width() - 2, 
                                            150 + key_icons[key].get_height() + 5))
        elif key == 'd': config.WINDOW.blit(key_icons[key], 
                                            (leftside_center + key_icons[key].get_width() - 1, 
                                            150 + key_icons[key].get_height() + 5))
        elif key == 'up': config.WINDOW.blit(key_icons[key], (rightside_center, 150))
        elif key == 'down' : config.WINDOW.blit(key_icons[key], 
                                                (rightside_center - 2, 150 + key_icons[key].get_height() + 5))
        elif key == 'left': config.WINDOW.blit(key_icons[key], 
                                            (rightside_center - key_icons[key].get_width() - 2, 
                                            150 + key_icons[key].get_height() + 5))
        elif key == 'right': config.WINDOW.blit(key_icons[key], 
                                            (rightside_center + key_icons[key].get_width() - 1, 
                                            150 + key_icons[key].get_height() + 5))
        elif key == 'shift': config.WINDOW.blit(key_icons[key], 
                                                (leftside_center - key_icons[key].get_width() // 2 + 13, 280))
        elif key == 'space': config.WINDOW.blit(key_icons[key], 
                                                (rightside_center - key_icons[key].get_width() // 2 + 15, 280))
        i += 1
    
    # draw player names
    text = player_name_font.render("Player 1", True, config.WHITE)
    config.WINDOW.blit(text, (leftside_center - 
                                text.get_width() // 2 + key_icons['w'].get_width() // 2, 60))
    text = player_name_font.render("Player 2", True, config.WHITE)
    config.WINDOW.blit(text, (rightside_center -
                                text.get_width() // 2 + key_icons['w'].get_width() // 2, 60))
    
    # draw decription text
    text = description_font.render("Movement", True, config.RED)
    config.WINDOW.blit(text, (80, 164))
    text = description_font.render("Movement", True, config.BLUE)
    config.WINDOW.blit(text, (config.WIDTH - 80 - text.get_width(), 164))
    text = description_font.render("Throw", True, config.RED)
    config.WINDOW.blit(text, (88, 278))
    text = description_font.render("Throw", True, config.BLUE)
    config.WINDOW.blit(text, (config.WIDTH - 110 - text.get_width(), 278))
        
def Handle_Ball(right_player, left_player):
    # allow players to grab ball
    right_player._Handle_Grab_Ball()
    left_player._Handle_Grab_Ball()

    # controls ball traveling across screen
    for i in range(config.DODGEBALL_NUMBERS):
        if left_player.Get_Ball(i).traveling:
            left_player.Get_Ball(i)._Travel()
            left_player.Get_Ball(i).Check_Hit(right_player)
        if right_player.Get_Ball(i).traveling:
            right_player.Get_Ball(i)._Travel()
            right_player.Get_Ball(i).Check_Hit(left_player)


def main():
    config.init()       # initialize global variables
    right_player = Player('RIGHT')
    left_player = Player('LEFT')

    # initialize buttons
    offset = 30     # distance between buttons
    button_ypos = 3 * (config.HEIGHT - 100) // 5
    play_button = Button(300, 100, config.WIDTH // 2 - 300 - offset, button_ypos, "Play")
    controls_button = Button(300, 100, config.WIDTH // 2 + offset, button_ypos, "Controls")
    back_button = Button(100, 50, 10, 10, "Back")

    clock = pygame.time.Clock()     # initialize clock
    run = True
    end_game = False       # ends game
    finish_game = False     # triggers game finsih animation

    # start menu variables
    start_game = False
    title_font = pygame.font.SysFont('times new roman', 100)
    title  = title_font.render("Dodgeball", True, config.BLACK)
    last_update = pygame.time.get_ticks()
    play_transitioning = False
    animation_stage = {'stage' : 0, 'frame' : 0}  # stage 0: cover screen; stage 1: uncover screen
    control_screen = False

    Initialize_Player_Animations()  
    key_icons = Extract_Key_Icons()
    Draw_Window()


    # start menu loop
    while not start_game:
        clock.tick(config.FPS)     # run clock   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_game = True
                run = False

        # draw main screen
        if not play_transitioning:
            config.WINDOW.blit(title, ((config.WIDTH - title.get_width()) // 2, config.HEIGHT // 5))
            play_pressed = play_button.Draw_Button()
            controls_pressed = controls_button.Draw_Button()

        current_time = pygame.time.get_ticks()

        # iterate through transition frames when play is pressed
        if play_pressed: play_transitioning = True
        if play_transitioning:
            if current_time - last_update >= 50:
                if animation_stage['stage'] == 1: Draw_Screen(left_player, right_player, end_game)
                Transition_Animation(animation_stage)
                animation_stage['frame'] += 1
                last_update = current_time
                if animation_stage['frame'] >= 20:
                    animation_stage['frame'] = 0
                    animation_stage['stage'] += 1
                    if animation_stage['stage'] >= 2: start_game = True
        
        # draw controls screen
        if controls_pressed: control_screen = True
        if control_screen:
            Draw_Window()
            back_transitioning = False
            back_pressed = back_button.Draw_Button()
            if back_pressed: back_transitioning = True
            if back_transitioning:
                control_screen = False
                Draw_Window()   
            else: 
                Draw_Control_Screen(key_icons)
        
        pygame.display.update()


    # game loop
    while run:
        clock.tick(config.FPS)     # run clock   

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == config.LEFT_PLAYER_HIT:
                left_player.current_action = 'hit'
                left_player.lives -= 1
                if left_player.dodgeball != None:
                    left_player.Get_Ball(left_player.dodgeball)._Delete()
                    left_player.dodgeball = None
                if left_player.lives <= 0: pygame.event.post(pygame.event.Event(config.END_GAME))
            if event.type == config.RIGHT_PLAYER_HIT:
                right_player.current_action = 'hit'
                right_player.lives -= 1
                if right_player.dodgeball != None:
                    right_player.Get_Ball(right_player.dodgeball)._Delete()
                    right_player.dodgeball = None
                if right_player.lives <= 0: pygame.event.post(pygame.event.Event(config.END_GAME))
            if event.type == config.END_GAME:
                right_player.current_action = 'idle'
                left_player.current_action = 'idle'
                finish_game = True
                pygame.time.delay(500)

        # handle ball and player movement
        if not finish_game:
            Handle_Ball(right_player, left_player)

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                right_player._Throw()
            if keys_pressed[pygame.K_LSHIFT]:
                left_player._Throw()
            if right_player.current_action != 'throw' or right_player.current_action != 'hit': 
                right_player._Handle_Movement(keys_pressed)
            if left_player.current_action != 'throw' or left_player.current_action != 'hit': 
                left_player._Handle_Movement(keys_pressed)    

        # update display
        if run != False: run = Draw_Screen(left_player, right_player, finish_game)
        pygame.display.update()
        if end_game: pygame.time.wait(5000)

    pygame.QUIT
    quit()

# program only runs if main.py is run directly
if __name__ == "__main__":
    main()