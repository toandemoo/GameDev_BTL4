from .board_evaluator import BoardEvaluator
from settings import *

INF = 10**9


class BoardSearcher:
    def __init__(self):
        self.evaluator = BoardEvaluator()
        self.board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.maxdepth = 3
        self.bestmove = None

    # =========================
    # CHECK WIN
    # =========================
    def isWin(self, row, col, turn):
        directions = [(1,0),(0,1),(1,1),(1,-1)]

        for dx, dy in directions:
            count = 1

            for d in [1, -1]:
                x, y = row, col
                while True:
                    x += dx*d
                    y += dy*d
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == turn:
                        count += 1
                    else:
                        break

            if count >= 5:
                return True

        return False

    # =========================
    # 🔥 TÌM NƯỚC THẮNG NGAY
    # =========================
    def findWinningMove(self, turn):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    self.board[i][j] = turn
                    if self.isWin(i, j, turn):
                        self.board[i][j] = 0
                        return (i, j)
                    self.board[i][j] = 0
        return None

    # =========================
    # HEURISTIC NHANH
    # =========================
    def quickEvaluate(self, row, col, turn):
        score = 0
        directions = [(1,0),(0,1),(1,1),(1,-1)]

        for dx, dy in directions:
            count_self = 1
            open_ends = 0

            for d in [1, -1]:
                x, y = row, col
                while True:
                    x += dx*d
                    y += dy*d
                    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                        if self.board[x][y] == turn:
                            count_self += 1
                        elif self.board[x][y] == 0:
                            open_ends += 1
                            break
                        else:
                            break
                    else:
                        break

            if count_self >= 5:
                score += 100000
            elif count_self == 4:
                score += 20000 if open_ends == 2 else 5000
            elif count_self == 3:
                score += 2000 if open_ends == 2 else 500
            elif count_self == 2:
                score += 200

        return score

    # =========================
    # GEN MOVES
    # =========================
    def genMoves(self, turn):
        moves = []
        board = self.board
        POSES = self.evaluator.POS

        candidates = set()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != 0:
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            x, y = i + dx, j + dy
                            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                                if board[x][y] == 0:
                                    candidates.add((x, y))

        if not candidates:
            center = BOARD_SIZE // 2
            return [(999999, center, center)]

        opponent = 2 if turn == 1 else 1

        # 🔥 ƯU TIÊN THẮNG NGAY
        for (i, j) in candidates:
            self.board[i][j] = turn
            if self.isWin(i, j, turn):
                self.board[i][j] = 0
                return [(999999, i, j)]
            self.board[i][j] = 0

        for (i, j) in candidates:
            score = POSES[i][j]

            attack = self.quickEvaluate(i, j, turn)

            self.board[i][j] = opponent
            defense = self.quickEvaluate(i, j, opponent)
            self.board[i][j] = 0

            score += attack + defense * 1.5
            moves.append((score, i, j))

        moves.sort(reverse=True)

        top = moves[0][0]
        moves = [m for m in moves if m[0] >= top * 0.5]

        return moves[:15]

    # =========================
    # MINIMAX
    # =========================
    def __search(self, turn, depth, alpha=-INF, beta=INF):

        # 🔥 check thắng ngay
        win_move = self.findWinningMove(turn)
        if win_move:
            return 9999

        score = self.evaluator.evaluate(self.board, turn)

        if abs(score) >= 9999 or depth == 0:
            return score

        moves = self.genMoves(turn)
        opponent = 2 if turn == 1 else 1

        bestmove = None

        for _, row, col in moves:

            self.board[row][col] = turn

            val = -self.__search(opponent, depth - 1, -beta, -alpha)

            self.board[row][col] = 0

            if val > alpha:
                alpha = val
                bestmove = (row, col)

                if alpha >= beta:
                    break

        if depth == self.maxdepth and bestmove:
            self.bestmove = bestmove

        return alpha

    # =========================
    # API CHÍNH
    # =========================
    def search(self, turn, depth=3):
        self.maxdepth = depth
        self.bestmove = None

        # 🔥 1. thắng ngay
        win_move = self.findWinningMove(turn)
        if win_move:
            return 9999, win_move[0], win_move[1]

        # 🔥 2. chặn ngay
        opponent = 2 if turn == 1 else 1
        block_move = self.findWinningMove(opponent)
        if block_move:
            return 0, block_move[0], block_move[1]

        score = self.__search(turn, depth)

        if self.bestmove is None:
            center = BOARD_SIZE // 2
            return 0, center, center

        row, col = self.bestmove
        return score, row, col