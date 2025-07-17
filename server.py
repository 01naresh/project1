# server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 65432
clients = []

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    while True:
        try:
            message = conn.recv(1024)
            broadcast(message, conn)
        except:
            clients.remove(conn)
            conn.close()
            break

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            client.send(message)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("[*] Server listening...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
