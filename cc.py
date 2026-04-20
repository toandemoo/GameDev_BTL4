import socket
import threading

HOST = "127.0.0.1"
PORT = 12345


def receive(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print("SERVER:", data.strip())
        except:
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

threading.Thread(target=receive, args=(client,), daemon=True).start()

while True:
    msg = input(">> ")
    client.send((msg + "\n").encode())