import random

def get_valid_moves(board):
    moves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                moves.append((row, col))
    return moves

def random_ai(board):
    moves = get_valid_moves(board)

    # ưu tiên ô giữa nếu còn
    center = (len(board)//2, len(board)//2)
    if center in moves:
        return center

    return random.choice(moves)