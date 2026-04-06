import math
import random
import time
from settings import *


# =========================
# NODE
# =========================
class Node:
    def __init__(self, board, turn, parent=None, move=None):
        self.board = board
        self.turn = turn
        self.parent = parent
        self.move = move

        self.children = []
        self.visits = 0
        self.wins = 0

    def ucb(self, c=1.4):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )


# =========================
# MCTS
# =========================
class MCTS:
    def __init__(self, board, turn, time_limit=1.2):
        self.root = Node([row[:] for row in board], turn)
        self.root_turn = turn
        self.time_limit = time_limit

    # =========================
    # CHECK WIN
    # =========================
    def isWin(self, board, row, col, turn):
        for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
            count = 1
            for d in [1, -1]:
                x, y = row, col
                while True:
                    x += dx*d
                    y += dy*d
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == turn:
                        count += 1
                    else:
                        break
            if count >= 5:
                return True
        return False

    # =========================
    # GEN MOVES (TỐI ƯU)
    # =========================
    def genMoves(self, board):
        moves = set()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != 0:
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            x, y = i + dx, j + dy
                            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                                if board[x][y] == 0:
                                    moves.add((x, y))

        if not moves:
            return [(BOARD_SIZE//2, BOARD_SIZE//2)]

        return list(moves)

    # =========================
    # 🔥 TÌM 1 NƯỚC THẮNG
    # =========================
    def findWinningMove(self, board, turn):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 0:
                    board[i][j] = turn
                    if self.isWin(board, i, j, turn):
                        board[i][j] = 0
                        return (i, j)
                    board[i][j] = 0
        return None

    # =========================
    # 🔥 TÌM TẤT CẢ NƯỚC THẮNG
    # =========================
    def findAllWinningMoves(self, board, turn):
        wins = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 0:
                    board[i][j] = turn
                    if self.isWin(board, i, j, turn):
                        wins.append((i, j))
                    board[i][j] = 0
        return wins

    # =========================
    # SELECTION
    # =========================
    def select(self, node):
        while node.children:
            node = max(node.children, key=lambda n: n.ucb())
        return node

    # =========================
    # EXPANSION (CHẶN + THẮNG)
    # =========================
    def expand(self, node):
        moves = self.genMoves(node.board)
        opponent = 2 if node.turn == 1 else 1

        # 🔥 chặn tuyệt đối
        opponent_wins = self.findAllWinningMoves(node.board, opponent)
        if opponent_wins:
            moves = opponent_wins
        else:
            # 🔥 ưu tiên thắng
            for move in moves:
                r, c = move
                node.board[r][c] = node.turn
                if self.isWin(node.board, r, c, node.turn):
                    node.board[r][c] = 0
                    moves = [move]
                    break
                node.board[r][c] = 0

        move = random.choice(moves)

        new_board = [row[:] for row in node.board]
        r, c = move
        new_board[r][c] = node.turn

        child = Node(
            new_board,
            opponent,
            parent=node,
            move=move
        )

        node.children.append(child)
        return child

    # =========================
    # SIMULATION (THÔNG MINH)
    # =========================
    def simulate(self, board, turn):
        board = [row[:] for row in board]

        for _ in range(30):
            opponent = 2 if turn == 1 else 1

            # thắng ngay
            move = self.findWinningMove(board, turn)
            if move:
                return turn

            # chặn ngay
            opponent_wins = self.findAllWinningMoves(board, opponent)
            if opponent_wins:
                r, c = random.choice(opponent_wins)
            else:
                moves = self.genMoves(board)
                if not moves:
                    return 0
                r, c = random.choice(moves)

            board[r][c] = turn

            if self.isWin(board, r, c, turn):
                return turn

            turn = opponent

        return 0

    # =========================
    # BACKPROP
    # =========================
    def backpropagate(self, node, result):
        while node:
            node.visits += 1
            if result == self.root_turn:
                node.wins += 1
            node = node.parent

    # =========================
    # SEARCH
    # =========================
    def search(self):
        # 🔥 thắng ngay
        win = self.findWinningMove(self.root.board, self.root.turn)
        if win:
            return win

        opponent = 2 if self.root.turn == 1 else 1

        # 🔥 chặn chắc chắn
        opponent_wins = self.findAllWinningMoves(self.root.board, opponent)
        if opponent_wins:
            return random.choice(opponent_wins)

        start = time.time()

        while time.time() - start < self.time_limit:
            node = self.select(self.root)

            node = self.expand(node)

            result = self.simulate(node.board, node.turn)

            self.backpropagate(node, result)

        # chọn node tốt nhất
        if not self.root.children:
            return random.choice(self.genMoves(self.root.board))

        best = max(self.root.children, key=lambda n: n.visits)
        return best.move