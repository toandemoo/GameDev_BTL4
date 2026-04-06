import pygame
from .AI_random import *
from .AI_MCTS import *
from .AI_MINIMAX import *
from settings import *


CELL_SIZE = 40

class Game:
    def __init__(self, screen):
        self.screen = screen
        
        self.broad = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.player = 1
        self.game_over = False
        
        self.board_width = len(self.broad[0]) * CELL_SIZE
        self.board_height = len(self.broad) * CELL_SIZE

        self.offset_x = (self.screen.get_width() - self.board_width) // 2 
        self.offset_y = (self.screen.get_height() - self.board_height) // 2
        
        self.ai = BoardSearcher()
        
        self.winner = 1
        
    def reset(self):
        self.broad = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.player = 1
        self.game_over = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # trừ offset để đưa về tọa độ board
            x -= self.offset_x
            y -= self.offset_y

            # nếu click ngoài board thì bỏ qua
            if x < 0 or y < 0 or x >= self.board_width or y >= self.board_height:
                return

            row = y // CELL_SIZE
            col = x // CELL_SIZE

            if not self.game_over:
                if row < BOARD_SIZE and col < BOARD_SIZE:
                    if self.broad[row][col] == 0 and self.player == 1:
                        self.broad[row][col] = self.player
                        self.player = 2

    def check_winner(self, board, player):
        size = len(board)

        for row in range(size):
            for col in range(size):

                if board[row][col] != player:
                    continue

                # ngang
                if col + 4 < size and all(board[row][col+i] == player for i in range(5)):
                    return True

                # dọc
                if row + 4 < size and all(board[row+i][col] == player for i in range(5)):
                    return True

                # chéo chính
                if row + 4 < size and col + 4 < size and all(board[row+i][col+i] == player for i in range(5)):
                    return True

                # chéo phụ
                if row + 4 < size and col - 4 >= 0 and all(board[row+i][col-i] == player for i in range(5)):
                    return True

        return False
    
    def update(self, level):
        if self.game_over:
            return
    
        if level == 3:
            if self.player == 2 and not self.game_over:

                # gán board cho AI
                self.ai.board = [row[:] for row in self.broad]

                score, row, col = self.ai.search(turn=2, depth=3)

                print("AI move:", row, col)

                if self.broad[row][col] == 0:
                    self.broad[row][col] = 2
                    self.player = 1
        
        if level == 2:
            if self.player == 2:
                # 🔥 tạo MCTS mới với board hiện tại
                mcts_ai = MCTS(self.broad, 2, time_limit=1.5)

                move = mcts_ai.search()

                if move:
                    row, col = move

                    if self.broad[row][col] == 0:
                        self.broad[row][col] = 2
                        self.player = 1
        
        if level == 1:
            if self.player == 2 and not self.game_over:
                move = random_ai(self.broad)

                if move:
                    r, c = move
                    self.broad[r][c] = 2
                    self.player = 1
                
        if self.check_winner(self.broad, 1):
            print("Player winner")
            self.winner = 1
            self.game_over = True

        if self.check_winner(self.broad, 2):
            print("AI winner")
            self.winner = 2
            self.game_over = True
         
    def draw(self):
        self.screen.fill((255,255,255))

        for row in range(len(self.broad)):
            for col in range(len(self.broad[row])):
                x = col * CELL_SIZE + self.offset_x
                y = row * CELL_SIZE + self.offset_y

                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

                if self.broad[row][col] == 1:
                    pygame.draw.circle(self.screen, (255, 0, 0), rect.center, CELL_SIZE//3)
                elif self.broad[row][col] == 2:
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, CELL_SIZE//3)
    
                    