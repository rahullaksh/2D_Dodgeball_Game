import pygame
import config
from playerClass import Player, Initialize_Player_Animations
pygame.font.init()


def Draw_Screen(player1, player2, end_game):
    # draw window
    draw_x_times = config.WIDTH // config.BACKGROUND.get_width() + 1
    draw_y_times = config.HEIGHT // config.BACKGROUND.get_height() + 1
    for y in range(draw_y_times):
        for x in range(draw_x_times):
            x_position = x * config.BACKGROUND.get_width()
            y_position = y * config.BACKGROUND.get_height()
            config.WINDOW.blit(config.BACKGROUND, (x_position, y_position))
    
    # draw text
    left_player_lives_text = config.LIVES_FONT.render("Lives: " + str(player1.lives), 1, (255, 255, 255))
    right_player_lives_text = config.LIVES_FONT.render("Lives: " + str(player2.lives), 1, (255, 255, 255))
    config.WINDOW.blit(left_player_lives_text, (5, 10))
    config.WINDOW.blit(right_player_lives_text, (config.WIDTH - right_player_lives_text.get_width() - 5, 10))
            
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
        if player1.lives <= 0: win_message = config.WIN_FONT.render("Right Player Wins!", 1, (255, 255, 255))
        else: win_message = config.WIN_FONT.render("Left Player Wins!", 1, (255, 255, 255))
        config.WINDOW.blit(win_message, (config.WIDTH // 2 - win_message.get_width() // 2, 
                                         config.HEIGHT // 2 - win_message.get_height() // 2))
        
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

    clock = pygame.time.Clock()     # initialize clock
    run = True
    end_game = False

    Initialize_Player_Animations()

    # game loop
    while run:
        clock.tick(config.FPS)     # run clock   

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
                end_game = True
                pygame.time.delay(1000)

        if not end_game:
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
        else:
            run = False  

        Draw_Screen(left_player, right_player, end_game)
        pygame.display.update()
        if end_game: pygame.time.wait(5000)

    pygame.QUIT
    quit()

# program only runs if main.py is run directly
if __name__ == "__main__":
    main()