import socket
import threading
from settings import *

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.clients = []
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = 0
        self.lock = threading.Lock()

    def broadcast(self, msg):
        for c in self.clients:
            try:
                c.send((msg + "\n").encode())
            except:
                pass




class CaroServer:
    DISCOVERY_PORT = 9999
    GAME_PORT = 5555

    def __init__(self):
        self.clients = []
        self.lock = threading.Lock()
        self.turn = 0  # 0 = X, 1 = O
        
        self.room_counter = 0
        self.rooms = {}   # 🔥 lưu tất cả room
        self.client_room = {}  # client → room

    # ================= SEND =================
    def send(self, conn, msg):
        conn.send((msg + "\n").encode())

    # ================= UDP DISCOVERY =================
    def discovery_server(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(("", self.DISCOVERY_PORT))

        print("🔍 Discovery server running...")

        while True:
            data, addr = udp.recvfrom(1024)

            if data == b"FIND_CARO_SERVER":
                udp.sendto(f"SERVER:{self.GAME_PORT}".encode(), addr)
                
    # =================ROOM==================
    def find_or_create_room(self):
        # tìm room còn chỗ
        for room in self.rooms.values():
            if len(room.clients) < 2:
                return room

        # nếu không có → tạo mới
        room_id = f"room{self.room_counter}"
        self.room_counter += 1

        room = Room(room_id)
        self.rooms[room_id] = room

        print(f"🆕 Created {room_id}")
        return room
    
    def remove_client(self, conn):
        if conn in self.client_room:
            room_id = self.client_room[conn]
            room = self.rooms[room_id]

            with room.lock:
                if conn in room.clients:
                    room.clients.remove(conn)

            del self.client_room[conn]

            # xóa room nếu rỗng
            if len(room.clients) == 0:
                print(f"🗑️ Remove {room_id}")
                del self.rooms[room_id]

    # ================= HANDLE CLIENT =================
    def handle_client(self, conn, addr):
        print("🎮 Connected:", addr)

        buffer = ""

        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break

                buffer += data

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()

                    if not line:
                        continue

                    if conn not in self.client_room:
                        continue

                    room_id = self.client_room[conn]
                    room = self.rooms[room_id]

                    if line.startswith("MOVE"):
                        _, r, c, role = line.split()
                        r, c = int(r), int(c)

                        with room.lock:
                            # kiểm tra lượt
                            if (role == "X" and room.turn == 0) or (role == "O" and room.turn == 1):

                                print(f"[{room_id}] {role} -> {r},{c}")

                                room.board[r][c] = 1 if role == "X" else 2

                                room.broadcast(line)

                                room.turn = 1 - room.turn

            except:
                break

        print("❌ Disconnect:", addr)

        self.remove_client(conn)
        conn.close()
    # def handle_client(self, conn, addr):
    #     print("🎮 Connected:", addr)

    #     buffer = ""

    #     while True:
    #         try:
    #             data = conn.recv(1024).decode()
    #             if not data:
    #                 break

    #             buffer += data

    #             while "\n" in buffer:
    #                 line, buffer = buffer.split("\n", 1)
    #                 line = line.strip()

    #                 if not line:
    #                     continue
                    
    #                 if line.startswith("WINNER"):
    #                     _, role = line.split()

    #                 if line.startswith("MOVE"):
    #                     _, r, c, role = line.split()

    #                     # kiểm tra lượt
    #                     if (role == "X" and self.turn == 0) or (role == "O" and self.turn == 1):

    #                         print(f"✔ VALID MOVE: {role} {r},{c}")

    #                         # gửi cho tất cả client
    #                         for c_conn in self.clients:
    #                             try:
    #                                 self.send(c_conn, line)
    #                             except:
    #                                 pass

    #                         # đổi lượt
    #                         self.turn = 1 - self.turn

    #         except:
    #             break

    #     print("❌ Disconnect:", addr)

    #     with self.lock:
    #         if conn in self.clients:
    #             self.clients.remove(conn)

    #     conn.close()

    # ================= TCP SERVER =================
    def game_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", self.GAME_PORT))
        server.listen()

        print("🚀 Game server running...")

        while True:
            conn, addr = server.accept()
            
            room = self.find_or_create_room()
            
            with room.lock:
                room.clients.append(conn)
                self.client_room[conn] = room.room_id

                if len(room.clients) == 1:
                    self.send(conn, "WAIT")

                elif len(room.clients) == 2:
                    room.turn = 0

                    self.send(room.clients[0], "ROLE X")
                    self.send(room.clients[1], "ROLE O")

                    room.broadcast("START")

            threading.Thread(
                target=self.handle_client,
                args=(conn, addr),
                daemon=True
            ).start()


            # with self.lock:
            #     if len(self.clients) >= 2:
            #         self.send(conn, "FULL")
            #         conn.close()
            #         continue

            #     self.clients.append(conn)

            #     if len(self.clients) == 1:
            #         self.send(conn, "WAIT")

            #     elif len(self.clients) == 2:
            #         self.turn = 0  # reset lượt

            #         # gán role
            #         self.send(self.clients[0], "ROLE X")
            #         self.send(self.clients[1], "ROLE O")

            #         # start game
            #         for c in self.clients:
            #             self.send(c, "START")

            # threading.Thread(
            #     target=self.handle_client,
            #     args=(conn, addr),
            #     daemon=True
            # ).start()

    # ================= RUN =================
    def run(self):
        threading.Thread(target=self.discovery_server, daemon=True).start()
        self.game_server()
    


if __name__ == "__main__":
    server = CaroServer()
    server.run()