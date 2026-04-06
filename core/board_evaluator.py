from settings import *

class BoardEvaluator(object):

    def __init__(self):
        self.POS = []
        center = BOARD_SIZE // 2

        # 🔥 cải thiện weight (mượt hơn)
        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                row.append(7 - (abs(i - center) + abs(j - center)))
            self.POS.append(tuple(row))

        # pattern
        self.cTwo = 1
        self.cThree = 2
        self.cFour = 3
        self.two = 4
        self.three = 5
        self.four = 6
        self.five = 7

        self.analyzed = 8
        self.unanalyzed = 0

        self.record = [[[0]*4 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.count = [[0]*10 for _ in range(3)]

        self.line = [0]*30
        self.result = [0]*30

        self.reset()

    def reset(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                for k in range(4):
                    self.record[i][j][k] = self.unanalyzed

        for i in range(3):
            for j in range(10):
                self.count[i][j] = 0

    # =========================
    # MAIN EVALUATE
    # =========================
    def evaluate(self, board, turn):
        score = self.__evaluate(board, turn)
        return score

    def __evaluate(self, board, turn):
        self.reset()

        record = self.record
        count = self.count

        # ===== analyze 4 directions =====
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] != 0:
                    if record[i][j][0] == 0:
                        self.__analysis_horizon(board, i)
                    if record[i][j][1] == 0:
                        self.__analysis_vertical(board, j)
                    if record[i][j][2] == 0:
                        self.__analysis_left(board, i, j)
                    if record[i][j][3] == 0:
                        self.__analysis_right(board, i, j)

        # ===== count pattern (fix overcount nhẹ) =====
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                stone = board[i][j]
                if stone != 0:
                    for k in range(4):
                        ch = record[i][j][k]
                        if ch in (self.five, self.four, self.cFour,
                                  self.three, self.cThree, self.two, self.cTwo):
                            count[stone][ch] += 1

        black = 1
        white = 2

        # ===== early win cutoff =====
        if count[black][self.five]:
            return -9999 if turn == white else 9999
        if count[white][self.five]:
            return 9999 if turn == white else -9999

        # 🔥 double-four
        if count[white][self.cFour] >= 2:
            count[white][self.four] += 1
        if count[black][self.cFour] >= 2:
            count[black][self.four] += 1

        # 🔥 double-three
        if count[white][self.three] >= 2:
            return 9960 if turn == white else -9960
        if count[black][self.three] >= 2:
            return -9960 if turn == white else 9960

        wvalue = 0
        bvalue = 0

        # ===== strong patterns =====
        if turn == white:
            if count[white][self.four]:
                return 9990
            if count[white][self.cFour]:
                return 9980
            if count[black][self.four]:
                return -9970
        else:
            if count[black][self.four]:
                return 9990
            if count[black][self.cFour]:
                return 9980
            if count[white][self.four]:
                return -9970

        # ===== heuristic =====
        def calc_value(cnt):
            return (cnt[self.three]*200 +
                    cnt[self.cThree]*50 +
                    cnt[self.two]*10 +
                    cnt[self.cTwo]*3)

        wvalue += calc_value(count[white])
        bvalue += calc_value(count[black])

        # ===== position weight =====
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == white:
                    wvalue += self.POS[i][j]
                elif board[i][j] == black:
                    bvalue += self.POS[i][j]

        # 🔥 bias theo lượt
        if turn == white:
            return int((wvalue - bvalue) * 1.1)
        else:
            return int((bvalue - wvalue) * 1.1)

    # =========================
    # ANALYSIS FUNCTIONS
    # =========================
    def __analysis_horizon(self, board, i):
        line = self.line[:BOARD_SIZE]
        for j in range(BOARD_SIZE):
            line[j] = board[i][j]

        self.analysis_line(line, self.result, BOARD_SIZE)

        for j in range(BOARD_SIZE):
            if self.result[j] != self.unanalyzed:
                self.record[i][j][0] = self.result[j]

    def __analysis_vertical(self, board, j):
        line = self.line[:BOARD_SIZE]
        for i in range(BOARD_SIZE):
            line[i] = board[i][j]

        self.analysis_line(line, self.result, BOARD_SIZE)

        for i in range(BOARD_SIZE):
            if self.result[i] != self.unanalyzed:
                self.record[i][j][1] = self.result[i]

    def __analysis_left(self, board, i, j):
        line = []
        size = BOARD_SIZE

        if i > j:
            x, y = 0, i - j
        else:
            x, y = j - i, 0

        while x < size and y < size:
            line.append(board[y][x])
            x += 1
            y += 1

        self.analysis_line(line, self.result, len(line))

    def __analysis_right(self, board, i, j):
        line = []
        size = BOARD_SIZE

        if i + j < size:
            x, y = 0, i + j
        else:
            x, y = i + j - (size - 1), size - 1

        while x < size and y >= 0:
            line.append(board[y][x])
            x += 1
            y -= 1

        self.analysis_line(line, self.result, len(line))

    # =========================
    # CORE LINE ANALYSIS (FIX BUG)
    # =========================
    def analysis_line(self, line, record, num):
        unanalyzed = self.unanalyzed

        # 🔥 FIX: reset sạch
        line = line[:num] + [-1]*(30 - num)
        for i in range(30):
            record[i] = unanalyzed

        if num < 5:
            return

        for i in range(num):
            if line[i] == 0:
                continue

            stone = line[i]
            count = 1

            # đếm liên tiếp
            j = i + 1
            while j < num and line[j] == stone:
                count += 1
                j += 1

            if count >= 5:
                record[i] = self.five
            elif count == 4:
                record[i] = self.four
            elif count == 3:
                record[i] = self.three
            elif count == 2:
                record[i] = self.two

            i = j