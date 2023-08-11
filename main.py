import pygame

WIDTH, HEIGHT = 900, 500
WINDOW =  pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodgeball")

FPS = 60

def Draw_Window():
    pass

def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        Draw_Window()
        pygame.display.update()

    pygame.QUIT

if __name__ == "__main__":
    main()