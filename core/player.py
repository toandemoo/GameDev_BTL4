import pygame

class Player:
    def __init__(self):
        self.img = pygame.image.load("assets/images/piece_x.png").convert_alpha()
        # img = pygame.transform.scale(img, (100, 100))

    def update():
        pass
    
    def draw(screen, x, y):
        screen.blit(self.img, (x, y))