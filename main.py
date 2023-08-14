import pygame
import config
import playerClass


def Draw_Screen(player1, player2):
    # draw window
    config.WINDOW.blit(config.BACKGROUND, (0, 0))
    pygame.draw.rect(config.WINDOW, config.BLACK, config.DIVIDER)

    # draw player
    config.WINDOW.blit(player1.player, (player1.hitbox.x, player1.hitbox.y))
    config.WINDOW.blit(player2.player, (player2.hitbox.x, player2.hitbox.y))


def main():
    config.init()       # initialize global variables
    right_player = playerClass.Player('RIGHT')
    left_player = playerClass.Player(player_section = 'LEFT')

    clock = pygame.time.Clock()     # initialize clock
    run = True

    # game loop
    while run:
        clock.tick(config.FPS)     # run clock   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        right_player.Handle_Movement(keys_pressed)
        left_player.Handle_Movement(keys_pressed)
        
        Draw_Screen(left_player, right_player)
        pygame.display.update()

    pygame.QUIT

# program only runs if main.py is run directly
if __name__ == "__main__":
    main()