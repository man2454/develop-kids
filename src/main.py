import pygame
from src.game import Game # Updated import path

def main():
    pygame.init()
    # It's good practice to initialize font module explicitly if using fonts heavily
    # pygame.font.init() # Though pygame.init() usually handles this.

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Quest of Knowledge")

    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT) # Pass screen dimensions
    clock = pygame.time.Clock() 

    while game.is_running:
        game.run(screen) 

        pygame.display.flip() 

        clock.tick(60) 

    pygame.quit()

if __name__ == '__main__':
    main()
