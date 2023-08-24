import pygame
import config
from playerClass import Player, Initialize_Player_Animations


def Draw_Screen(player1, player2):
    # draw window
    draw_x_times = config.WIDTH // config.BACKGROUND.get_width() + 1
    draw_y_times = config.HEIGHT // config.BACKGROUND.get_height() + 1
    for y in range(draw_y_times):
        for x in range(draw_x_times):
            x_position = x * config.BACKGROUND.get_width()
            y_position = y * config.BACKGROUND.get_height()
            config.WINDOW.blit(config.BACKGROUND, (x_position, y_position))

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
        
def Handle_Ball(right_player, left_player):
    # allow players to grab ball
    right_player._Handle_Grab_Ball()
    left_player._Handle_Grab_Ball()

    # controls ball traveling across screen
    for i in range(config.DODGEBALL_NUMBERS):
        if left_player.Get_Ball(i).traveling:
            left_player.Get_Ball(i)._Travel(left_player)
        if right_player.Get_Ball(i).traveling:
            right_player.Get_Ball(i)._Travel(right_player)


def main():
    config.init()       # initialize global variables
    right_player = Player('RIGHT')
    left_player = Player('LEFT')

    clock = pygame.time.Clock()     # initialize clock
    run = True

    Initialize_Player_Animations()

    # game loop
    while run:
        clock.tick(config.FPS)     # run clock   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    right_player._Throw()
                if event.key == pygame.K_LSHIFT:
                    left_player._Throw()            

        Handle_Ball(right_player, left_player)

        keys_pressed = pygame.key.get_pressed()
        if right_player.current_action != 'throw': right_player._Handle_Movement(keys_pressed)
        if left_player.current_action != 'throw': left_player._Handle_Movement(keys_pressed)
        
        Draw_Screen(left_player, right_player)
        pygame.display.update()

    pygame.QUIT
    quit()

# program only runs if main.py is run directly
if __name__ == "__main__":
    main()