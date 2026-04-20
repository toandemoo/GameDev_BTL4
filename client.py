import socket
import threading
from settings import *
from queue import Queue

CELL_SIZE = 40

class CaroClient:
    DISCOVERY_PORT = 9999

    def __init__(self):
        self.board = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.role = None
        self.your_turn = False
        self.client = None
        self.enemy_hit_queue = Queue()

    # ================= FIND SERVER =================
    def find_server(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp.settimeout(3)

        udp.sendto(b"FIND_CARO_SERVER", ("255.255.255.255", self.DISCOVERY_PORT))

        try:
            data, addr = udp.recvfrom(1024)
            port = int(data.decode().split(":")[1])
            print("✅ Found server:", addr[0], port)
            return addr[0], port
        except:
            print("❌ Not Found server")
            return None

    # ================= BOARD =================
    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

    def update_board(self, r, c, symbol):
        self.board[r][c] = symbol

    # ================= RECEIVE =================
    def receive(self):
        buffer = ""

        while True:
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    print("Server close connect")
                    break

                buffer += data

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()

                    if not line:
                        continue

                    # ================= HANDLE =================
                    if line == "WAIT":
                        print("⏳ Wait Player...")

                    elif line.startswith("ROLE"):
                        self.role = line.split()[1]
                        print(f"🎭 You are: {self.role}")

                    elif line == "START":
                        print("🎮 Game Start!")

                        if self.role == "X":
                            self.your_turn = True
                            print("Your turn!")
                        else:
                            self.your_turn = False

                    elif line.startswith("MOVE"):
                        _, r, c, move_role = line.split()
                        r, c = int(r), int(c)
                        print("Enemy Hit:", r, c)
                        self.enemy_hit_queue.put((r, c))

                        # print(f"🎯 {move_role} hit: {r},{c}")
                        self.update_board(r, c, move_role)
                        # self.print_board()

                        if move_role != self.role:
                            self.your_turn = True
                            print("Your Turn")

            except Exception as e:
                print("Error:", e)
                break
    
    # def receive(self):
    #     buffer = ""

    #     while True:
    #         try:
    #             data = self.client.recv(1024).decode()
    #             if not data:
    #                 print("Server close connect")
    #                 break

    #             buffer += data

    #             while "\n" in buffer:
    #                 line, buffer = buffer.split("\n", 1)
    #                 line = line.strip()

    #                 if not line:
    #                     continue

    #                 # ================= HANDLE =================
    #                 if line == "WAIT":
    #                     print("⏳ Wait Player...")

    #                 elif line.startswith("ROLE"):
    #                     self.role = line.split()[1]
    #                     print(f"🎭 You are: {self.role}")

    #                 elif line == "START":
    #                     print("🎮 Game Start!")

    #                     # reset board khi vào room mới
    #                     self.board = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    #                     if self.role == "X":
    #                         self.your_turn = True
    #                         print("Your turn!")
    #                     else:
    #                         self.your_turn = False

    #                 # 🔥 FIX QUAN TRỌNG
    #                 elif line.startswith("UPDATE"):
    #                     _, r, c, player = line.split()
    #                     r, c = int(r), int(c)

    #                     symbol = "X" if player == "1" else "O"

    #                     print(f"📥 Update: {symbol} {r},{c}")

    #                     # đưa vào queue (để pygame xử lý)
    #                     self.enemy_hit_queue.put((r, c))

    #                     # update board
    #                     self.update_board(r, c, symbol)

    #                     # đổi lượt
    #                     if symbol != self.role:
    #                         self.your_turn = True
    #                         print("👉 Your turn!")

    #         except Exception as e:
    #             print("Error:", e)
    #             break
    
    # ================= RUN =================
    def connect_server(self):
        result = self.find_server()
        if not result:
            return

        ip, port = result

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

        threading.Thread(target=self.receive, daemon=True).start()
    
    def run(self, row, col):
        # while True:
            if self.your_turn:
                try:
                    # move = input("Nhập nước đi (row col): ")
                    # r, c = map(int, move.split())

                    if self.board[row][col] != ".":
                        print("O da danh!")
                        # continue

                    # 🔥 FIX: phải có \n
                    self.client.send(f"MOVE {row} {col} {self.role}\n".encode())
                    print(f"You Hit: {row} {col}")

                    self.your_turn = False

                except:
                    print("Sai format!")
                    
    # def run(self, row, col):
    #     if not self.your_turn:
    #         return

    #     if self.board[row][col] != ".":
    #         print("❌ Ô đã đánh!")
    #         return

    #     try:
    #         self.client.send(f"MOVE {row} {col} {self.role}\n".encode())
    #         print(f"📤 You Hit: {row} {col}")

    #         self.your_turn = False

    #     except:
    #         print("Send error")
    
    def winner(self, role):
        self.your_turn = False
        self.client.send(f"WINNER {role}\n".encode())


# if __name__ == "__main__":
#     client = CaroClient()
#     client.run()