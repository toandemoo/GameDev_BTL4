from settings import *
import socket
import threading
from queue import Queue

HOST = "0.0.0.0"
PORT = 12345

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.client = None
        self.turn = 2  # 0: player1, 1: player2
        # self.board = board
        self.lock = threading.Lock()
        self.queue = Queue()

    def init_server(self):
        self.server.bind((HOST, PORT))
        self.server.listen()
        print("Server running...")

    def start_server(self):
        while len(self.clients) < 2:
            client, addr = self.server.accept()
            self.clients.append(client)
            self.client = client
            print("Connected:", addr)

            # tạo thread cho mỗi client
            threading.Thread(
                target=self.handle_client,
                args=(client,),
                daemon=True
            ).start()
    
    def broadcast(self, msg):
        for c in self.clients:
            try:
                c.send(msg.encode())
            except:
                pass

    def handle_client(self, client, player_id = 2):
        symbol = 2 if player_id == 2 else 1
        client.send(f"START {symbol}\n".encode())

        buffer = ""

        while True:
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    break

                buffer += data

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    parts = line.strip().split()

                    if parts[0] == "MOVE":
                        row, col = int(parts[1]), int(parts[2])

                        with self.lock:
                            self.queue.put((row, col, player_id))

                        print("Received MOVE:", row, col)

                        # 🔥 gửi lại cho tất cả client (broadcast)
                        self.broadcast(f"MOVE {row} {col}\n")

            except Exception as e:
                print("ERROR:", e)
                break

        client.close()