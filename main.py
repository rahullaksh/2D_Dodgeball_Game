import pygame
import config
from playerClass import Player


def Draw_Screen(player1, player2):
    # draw window
    config.WINDOW.blit(config.BACKGROUND, (0, 0))
    pygame.draw.rect(config.WINDOW, config.BLACK, config.DIVIDER)

    # draw player
    config.WINDOW.blit(player1.player, (player1.hitbox.x, player1.hitbox.y))
    config.WINDOW.blit(player2.player, (player2.hitbox.x, player2.hitbox.y))

    # draw balls
    for i in range(config.DODGEBALL_NUMBERS):
        config.WINDOW.blit(player1.Get_Ball(i).ball, (player1.Get_Ball(i).hitbox.x, 
                                                player1.Get_Ball(i).hitbox.y))
        config.WINDOW.blit(player2.Get_Ball(i).ball, (player2.Get_Ball(i).hitbox.x, 
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
        right_player._Handle_Movement(keys_pressed)
        left_player._Handle_Movement(keys_pressed)
        
        Draw_Screen(left_player, right_player)
        pygame.display.update()

    pygame.QUIT

# program only runs if main.py is run directly
if __name__ == "__main__":
    main()