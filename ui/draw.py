import pygame

def draw_board(screen):
    img = pygame.image.load("assets/images/broad.png").convert_alpha()
    # img = pygame.transform.scale(img, (100, 100))
    screen.blit(img, (0, 0))
        