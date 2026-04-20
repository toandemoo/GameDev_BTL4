import pygame
from core.game import Game
from settings import *
# from ui.draw import *
# from core.broad import * 
from menu import * 
from server import *
from client import *

# Main
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board Game AI")

clock = pygame.time.Clock()
game = Game(screen)
menu = Menu(screen)

# # Game Online
# server = CaroServer()
# server.run()

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not menu.game_start or not menu.option:
            menu.handle_event_start(event, game)
            if menu.option:
                menu.handle_event_playing(event, game)
        
        elif not menu.handle_event_playing(event, game):
            if not menu.pause:
                game.handle_event(event)

    menu.draw()
    menu.draw_option()

    if menu.game_start and menu.option:
        if not menu.pause:
            game.update(menu.level)
        
        game.draw()
        game.draw_Your_turn_play_online(screen)
        menu.draw_pause()
    
        if game.game_over:
            menu.draw_result(game)

    pygame.display.flip()

pygame.quit()