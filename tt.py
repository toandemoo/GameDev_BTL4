import socket
import threading

HOST = "0.0.0.0"
PORT = 12345
SIZE = 10


# ================= ROOM =================
class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.clients = []
        self.board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.turn = 0
        self.lock = threading.Lock()

    def broadcast(self, msg):
        for c in self.clients:
            try:
                c.send((msg + "\n").encode())
            except:
                pass


# ================= SERVER =================
class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rooms = {}            # room_id -> Room
        self.client_room = {}      # client -> room_id

    def start(self):
        self.server.bind((HOST, PORT))
        self.server.listen()
        print("Server running...")

        while True:
            client, addr = self.server.accept()
            print("Connected:", addr)

            threading.Thread(
                target=self.handle_client,
                args=(client,),
                daemon=True
            ).start()

    def handle_client(self, client):
        try:
            while True:
                data = client.recv(1024).decode()
                if not data:
                    break

                parts = data.strip().split()

                # ================= CREATE ROOM =================
                if parts[0] == "CREATE":
                    room_id = parts[1]

                    if room_id not in self.rooms:
                        self.rooms[room_id] = Room(room_id)

                    room = self.rooms[room_id]
                    room.clients.append(client)
                    self.client_room[client] = room_id

                    client.send(f"CREATED {room_id}\n".encode())

                # ================= JOIN ROOM =================
                elif parts[0] == "JOIN":
                    room_id = parts[1]

                    if room_id in self.rooms:
                        room = self.rooms[room_id]
                        room.clients.append(client)
                        self.client_room[client] = room_id

                        client.send(f"JOINED {room_id}\n".encode())

                        # nếu đủ 2 người → start game
                        if len(room.clients) == 2:
                            room.broadcast("START\n")
                    else:
                        client.send("ROOM_NOT_FOUND\n".encode())

                # ================= MOVE =================
                elif parts[0] == "MOVE":
                    row, col = int(parts[1]), int(parts[2])

                    if client not in self.client_room:
                        continue

                    room_id = self.client_room[client]
                    room = self.rooms[room_id]

                    with room.lock:
                        if room.board[row][col] == 0:
                            player = room.clients.index(client) + 1
                            room.board[row][col] = player

                            room.broadcast(f"UPDATE {row} {col} {player}")

                # ================= EXIT =================
                elif parts[0] == "EXIT":
                    self.remove_client(client)
                    break

        except:
            pass

        self.remove_client(client)
        client.close()

    def remove_client(self, client):
        if client in self.client_room:
            room_id = self.client_room[client]
            room = self.rooms[room_id]

            if client in room.clients:
                room.clients.remove(client)

            del self.client_room[client]

            # nếu room rỗng → xóa
            if len(room.clients) == 0:
                del self.rooms[room_id]


if __name__ == "__main__":
    Server().start()