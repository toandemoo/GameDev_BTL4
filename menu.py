import pygame
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        screen_rect = self.screen.get_rect()
        
        self.bg = pygame.image.load("assets/images/bg_intro.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (400, 300))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.center = screen_rect.center
        self.bg_rect.y -= 50
        
        
        self.btn = pygame.image.load("assets/images/start_btn.png").convert_alpha()
        self.btn = pygame.transform.scale(self.btn, (150, 50))
        self.btn_rect = self.btn.get_rect()
        self.btn_rect.center = screen_rect.center
        self.btn_rect.y += 150
        
        self.pause_btn = pygame.image.load("assets/images/pause_btn.png").convert_alpha()
        self.pause_btn = pygame.transform.scale(self.pause_btn, (30, 30))
        self.pause_btn_rect = self.pause_btn.get_rect()
        self.pause_btn_rect.x = screen_rect.w - 50
        self.pause_btn_rect.y = 20
        
        self.pause_text = pygame.image.load("assets/images/pause_text.png").convert_alpha()
        self.pause_text = pygame.transform.scale(self.pause_text, (240, 100))
        self.pause_text_rect = self.pause_text.get_rect()
        self.pause_text_rect.center = screen_rect.center
        self.pause_text_rect.y -= 50
        
        self.continue_btn = pygame.image.load("assets/images/playcontinue_btn.png").convert_alpha()
        self.continue_btn = pygame.transform.scale(self.continue_btn, (200, 50))
        self.continue_btn_rect = self.continue_btn.get_rect()
        self.continue_btn_rect.center = screen_rect.center
        self.continue_btn_rect.y = self.pause_text_rect.bottom + 30
        
        
        self.winner_text = pygame.image.load("assets/images/winner.png").convert_alpha()
        self.winner_text = pygame.transform.scale(self.winner_text, (240, 100))
        self.winner_text_rect = self.winner_text.get_rect()
        self.winner_text_rect.center = screen_rect.center
        self.winner_text_rect.y -= 50
        
        self.gameover_text = pygame.image.load("assets/images/gameover.png").convert_alpha()
        self.gameover_text = pygame.transform.scale(self.gameover_text, (240, 100))
        self.gameover_text_rect = self.gameover_text.get_rect()
        self.gameover_text_rect.center = screen_rect.center
        self.gameover_text_rect.y -= 50
        
        self.playagain_btn = pygame.image.load("assets/images/playagain_btn.png").convert_alpha()
        self.playagain_btn = pygame.transform.scale(self.playagain_btn, (200, 50))
        self.playagain_btn_rect = self.playagain_btn.get_rect()
        self.playagain_btn_rect.center = screen_rect.center
        self.playagain_btn_rect.y = self.winner_text_rect.bottom + 20
        
        self.exit_btn = pygame.image.load("assets/images/exit_btn.png").convert_alpha()
        self.exit_btn = pygame.transform.scale(self.exit_btn, (200, 50))
        self.exit_btn_rect = self.exit_btn.get_rect()
        self.exit_btn_rect.center = screen_rect.center
        self.exit_btn_rect.y = self.playagain_btn_rect.bottom + 20
        
        self.gameover_text = pygame.image.load("assets/images/gameover.png").convert_alpha()
        self.gameover_text = pygame.transform.scale(self.gameover_text, (240, 100))
        self.gameover_text_rect = self.gameover_text.get_rect()
        self.gameover_text_rect.center = screen_rect.center
        self.gameover_text_rect.y -= 50
        
        self.options_text = pygame.image.load("assets/images/options_text.png").convert_alpha()
        self.options_text = pygame.transform.scale(self.options_text, (240, 100))
        self.options_text_rect = self.options_text.get_rect()
        self.options_text_rect.center = screen_rect.center
        self.options_text_rect.y -= 100
        
        
        self.easy_btn = pygame.image.load("assets/images/easy_btn.png").convert_alpha()
        self.easy_btn = pygame.transform.scale(self.easy_btn, (200, 50))
        self.easy_btn_rect = self.easy_btn.get_rect()
        self.easy_btn_rect.center = screen_rect.center
        self.easy_btn_rect.y = self.options_text_rect.bottom + 20
        
        self.medium_btn = pygame.image.load("assets/images/medium_btn.png").convert_alpha()
        self.medium_btn = pygame.transform.scale(self.medium_btn, (200, 50))
        self.medium_btn_rect = self.medium_btn.get_rect()
        self.medium_btn_rect.center = screen_rect.center
        self.medium_btn_rect.y = self.easy_btn_rect.bottom + 20
        
        self.advance_btn = pygame.image.load("assets/images/advance_btn.png").convert_alpha()
        self.advance_btn = pygame.transform.scale(self.advance_btn, (200, 50))
        self.advance_btn_rect = self.advance_btn.get_rect()
        self.advance_btn_rect.center = screen_rect.center
        self.advance_btn_rect.y = self.medium_btn_rect.bottom + 20
        
        self.playonline_btn = pygame.image.load("assets/images/playonline_btn.png").convert_alpha()
        self.playonline_btn = pygame.transform.scale(self.playonline_btn, (200, 50))
        self.playonline_btn_rect = self.playonline_btn.get_rect()
        self.playonline_btn_rect.center = screen_rect.center
        self.playonline_btn_rect.y = self.advance_btn_rect.bottom + 20
        
        self.view_result_img = pygame.image.load("assets/images/viewresult_btn.png").convert_alpha()
        self.back_img = pygame.image.load("assets/images/back_btn.png").convert_alpha()
        self.viewresult_btn = pygame.image.load("assets/images/viewresult_btn.png").convert_alpha()
        self.viewresult_btn = pygame.transform.scale(self.viewresult_btn, (200, 50))
        self.viewresult_btn_rect = self.viewresult_btn.get_rect()
        self.viewresult_btn_rect.center = screen_rect.center
        self.viewresult_btn_rect.y = self.exit_btn_rect.bottom + 20
        
        self.game_start = False
        self.pause = False
        self.option = False
        self.view_result = True
        self.level = 0
        
    def handle_event_start(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            if not self.game_start and self.btn_rect.collidepoint(x, y):
                self.game_start = True
                self.option = False
                game.reset()
                return True

            elif self.game_start and not self.option:
                if self.easy_btn_rect.collidepoint(x, y):
                    self.level = 1
                    self.option = True
                    return True
                elif self.medium_btn_rect.collidepoint(x, y):
                    self.level = 2
                    self.option = True
                    return True
                elif self.advance_btn_rect.collidepoint(x, y):
                    self.level = 3
                    self.option = True
                    return True
                elif self.playonline_btn_rect.collidepoint(x, y):
                    self.level = 4
                    self.option = True
                    return True
                
    def handle_event_playing(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if self.game_start and self.pause_btn_rect.collidepoint(x, y):
                if not self.pause:
                    self.pause = True
                    print("pause click")
                    return True

            elif self.game_start and self.continue_btn_rect.collidepoint(x, y):
                if self.pause:
                    self.pause = False
                    print("continue click")
                    return True
            
            if not self.game_start and self.continue_btn_rect.collidepoint(x, y):
                self.game_start = True
                self.pause = False
                print("continue click")
                return True

            if game.game_over and self.playagain_btn_rect.collidepoint(x, y):
                game.reset()
                return True
            
            if game.game_over and self.exit_btn_rect.collidepoint(x, y):
                self.game_start = False
                game.reset()
                self.option = False
                self.pause = False
                return True
            
            if game.game_over and self.viewresult_btn_rect.collidepoint(x, y):
                self.view_result = not self.view_result
                if not self.view_result:
                    self.viewresult_btn = self.back_img
                    self.viewresult_btn = pygame.transform.scale(self.viewresult_btn, (200, 50))
                    self.viewresult_btn.set_alpha(128)
                else:
                    self.viewresult_btn = self.view_result_img
                    self.viewresult_btn = pygame.transform.scale(self.viewresult_btn, (200, 50))
                return True
            
            if self.pause and self.exit_btn_rect.collidepoint(x, y):
                self.game_start = False
                self.pause = False
                return True
            
        return False
        
    def draw(self):
        if not self.game_start:
            self.screen.fill((255,255,255))
            self.screen.blit(self.bg, self.bg_rect)
            self.screen.blit(self.btn, self.btn_rect)
            if self.option:
                self.continue_btn_rect.y = self.btn_rect.y - 55
                self.screen.blit(self.continue_btn, self.continue_btn_rect)
            
    def draw_option(self):
        if self.game_start and not self.option:
            self.screen.fill((255,255,255))
            self.screen.blit(self.options_text, self.options_text_rect)
            self.screen.blit(self.easy_btn, self.easy_btn_rect)
            self.screen.blit(self.medium_btn, self.medium_btn_rect)
            self.screen.blit(self.advance_btn, self.advance_btn_rect)
            self.screen.blit(self.playonline_btn, self.playonline_btn_rect)
            
    def draw_pause(self):
        self.screen.blit(self.pause_btn, self.pause_btn_rect)
        if self.pause:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)  # độ trong suốt (0-255)
            overlay.fill((0, 0, 0))  # màu đen

            self.screen.blit(overlay, (0, 0))
            
            self.screen.blit(self.pause_text, self.pause_text_rect)
            self.continue_btn_rect.y = self.pause_text_rect.bottom + 30
            self.screen.blit(self.continue_btn, self.continue_btn_rect)
            self.screen.blit(self.exit_btn, self.exit_btn_rect)
    
    def draw_result(self, game):
        if self.view_result:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)  # độ trong suốt (0-255)
            overlay.fill((0, 0, 0))  # màu đen
            self.screen.blit(overlay, (0, 0))
            if game.playOnline():
                if game.winner == game.player:
                    self.screen.blit(self.winner_text, self.winner_text_rect)
                else:
                    self.screen.blit(self.gameover_text, self.gameover_text_rect)
            else:
                if game.winner == 1:
                    self.screen.blit(self.winner_text, self.winner_text_rect)
                else:
                    self.screen.blit(self.gameover_text, self.gameover_text_rect)
            
            self.screen.blit(self.playagain_btn, self.playagain_btn_rect)
            self.screen.blit(self.exit_btn, self.exit_btn_rect)
        self.screen.blit(self.viewresult_btn, self.viewresult_btn_rect)
            
    