import socket
import threading
import time
from settings import *
from core.AI_MINIMAX import *

HOST = "172.20.10.2"
PORT = 12345

board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
ai = BoardSearcher()

move = None
lock = threading.Lock()
my_turn = False


def receive_data(client):
    global move, my_turn
    
    buffer = ""

    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            
            buffer += data 
            
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                parts = line.strip().split()

                if parts[0] == "START":
                    my_symbol = parts[1]
                    print(f"You are {my_symbol}")

                    # giả sử player 2 đi sau
                    if my_symbol == "2":
                        my_turn = False
                    else:
                        my_turn = True

                elif parts[0] == "UPDATE":
                    x, y = int(parts[1]), int(parts[2])
                    board[x][y] = 1
                    my_turn = True
                    print(f"Enemy: {x} {y}")

                elif parts[0] == "WIN":
                    print("Winner:", parts[1])
                    break

        except:
            break


def start_client():
    global move, my_turn

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    threading.Thread(target=receive_data, args=(client,), daemon=True).start()

    while True:
        if my_turn:
            print("AI thinking...")
            
            ai.board = [row[:] for row in board]

            score, row, col = ai.search(turn=2, depth=3)

            board[row][col] = 2

            with lock:
                move = (row, col)

            client.send(f"MOVE {row} {col}\n".encode())
            print("Sent:", row, col)

            my_turn = False

        time.sleep(0.1)


if __name__ == "__main__":
    
    start_client()