import pygame
from core.game import Game
from settings import *
from ui.draw import *
from core.broad import * 
from menu import * 

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board Game AI")

clock = pygame.time.Clock()
game = Game(screen)
menu = Menu(screen)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 🎯 MENU ưu tiên khi:
        # - chưa start
        # - đang pause
        # - chưa chọn level
        # if menu.game_start and not menu.pause and not game.game_over: 
        #     game.handle_event(event) 
        # start screen
        # option screen
        # pause screen
        # result screen
        
        if not menu.game_start or not menu.option:
            menu.handle_event_start(event, game)
        
        elif not menu.handle_event_playing(event, game):
            if not menu.pause:
                game.handle_event(event)

    menu.draw()
    menu.draw_option()

    if menu.game_start and menu.option:
        if not menu.pause:
            game.update(menu.level)
        
        game.draw()
        menu.draw_pause()
    
        if game.game_over:
            menu.draw_result(game.winner)

    pygame.display.flip()

pygame.quit()