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
        self.untried_moves = []

        self.visits = 0
        self.wins = 0

    def ucb(self, c=1.0):
        if self.visits == 0:
            return float('inf')

        prior = 0.05 * (self.wins / (self.visits + 1))

        return (self.wins / self.visits) + prior + c * math.sqrt(
            math.log(self.parent.visits + 1) / self.visits
        )


# =========================
# MCTS
# =========================
class MCTS:
    def __init__(self, board, turn, time_limit=1.5):
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
    # HEURISTIC (ATTACK + DEFEND)
    # =========================
    def evaluateMove(self, board, r, c, turn):
        opponent = 2 if turn == 1 else 1
        score = 0

        for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
            count_self = 0
            count_oppo = 0

            for d in [1, -1]:
                x, y = r, c
                while True:
                    x += dx*d
                    y += dy*d
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                        if board[x][y] == turn:
                            count_self += 1
                        elif board[x][y] == opponent:
                            count_oppo += 1
                            break
                        else:
                            break
                    else:
                        break

            if count_self >= 4:
                score += 100000
            elif count_self == 3:
                score += 5000
            elif count_self == 2:
                score += 200

            if count_oppo >= 4:
                score += 90000
            elif count_oppo == 3:
                score += 4000

        return score

    # =========================
    # DOUBLE THREAT
    # =========================
    def isDoubleThreat(self, board, r, c, turn):
        threats = 0
        board[r][c] = turn

        for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
            count = 1
            for d in [1, -1]:
                x, y = r, c
                while True:
                    x += dx*d
                    y += dy*d
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == turn:
                        count += 1
                    else:
                        break

            if count >= 4:
                threats += 1

        board[r][c] = 0
        return threats >= 2

    # =========================
    # GEN MOVES
    # =========================
    def genMoves(self, board):
        moves = set()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != 0:
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            x, y = i + dx, j + dy
                            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                                if board[x][y] == 0:
                                    moves.add((x, y))

        if not moves:
            return [(BOARD_SIZE//2, BOARD_SIZE//2)]

        center = BOARD_SIZE // 2
        return sorted(moves, key=lambda m: abs(m[0]-center)+abs(m[1]-center))

    # =========================
    # WIN MOVE
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
    # SELECT
    # =========================
    def select(self, node):
        while node.children and not node.untried_moves:
            node = max(node.children, key=lambda n: n.ucb())
        return node

    # =========================
    # EXPAND
    # =========================
    def expand(self, node):
        if not node.untried_moves:
            moves = self.genMoves(node.board)
            opponent = 2 if node.turn == 1 else 1

            moves = sorted(
                moves,
                key=lambda m: self.evaluateMove(node.board, m[0], m[1], node.turn)
                              + 0.8 * self.evaluateMove(node.board, m[0], m[1], opponent),
                reverse=True
            )

            node.untried_moves = moves[:20]

        if node.untried_moves:
            move = node.untried_moves.pop(0)
        else:
            move = random.choice(node.children).move

        opponent = 2 if node.turn == 1 else 1

        new_board = [row[:] for row in node.board]
        r, c = move
        new_board[r][c] = node.turn

        child = Node(new_board, opponent, node, move)
        node.children.append(child)
        return child

    # =========================
    # SIMULATE (SMART ROLLOUT)
    # =========================
    def simulate(self, board, turn):
        board = [row[:] for row in board]

        for _ in range(20):
            opponent = 2 if turn == 1 else 1

            move = self.findWinningMove(board, turn)
            if move:
                return turn

            opponent_wins = self.findAllWinningMoves(board, opponent)
            if opponent_wins:
                r, c = opponent_wins[0]
            else:
                moves = self.genMoves(board)
                moves = sorted(
                    moves,
                    key=lambda m: self.evaluateMove(board, m[0], m[1], turn),
                    reverse=True
                )[:2]

                if not moves:
                    return 0

                r, c = moves[0]

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
    # ROOT REUSE
    # =========================
    def update_root(self, move):
        for child in self.root.children:
            if child.move == move:
                self.root = child
                self.root.parent = None
                return

        new_board = [row[:] for row in self.root.board]
        r, c = move
        new_board[r][c] = self.root.turn
        self.root = Node(new_board, 2 if self.root.turn == 1 else 1)

    # =========================
    # SEARCH
    # =========================
    def search(self):
        # thắng ngay
        win = self.findWinningMove(self.root.board, self.root.turn)
        if win:
            return win

        opponent = 2 if self.root.turn == 1 else 1

        # chặn ngay
        opponent_wins = self.findAllWinningMoves(self.root.board, opponent)
        if opponent_wins:
            return opponent_wins[0]

        # double threat
        for move in self.genMoves(self.root.board):
            r, c = move
            if self.isDoubleThreat(self.root.board, r, c, self.root.turn):
                return move

        start = time.time()

        while time.time() - start < self.time_limit:
            node = self.select(self.root)
            node = self.expand(node)
            result = self.simulate(node.board, node.turn)
            self.backpropagate(node, result)

        best = max(self.root.children, key=lambda n: n.visits)
        return best.move