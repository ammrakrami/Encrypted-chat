import socket
import threading
from cryptography.fernet import Fernet

# Generate encryption key
key = Fernet.generate_key()
cipher = Fernet(key)

print(f"[KEY] Share this key with client: {key.decode()}")

host = "0.0.0.0"
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

def handle_client(client_socket):
    while True:
        try:
            encrypted_msg = client_socket.recv(1024)
            if not encrypted_msg:
                break

            # Decrypt message
            message = cipher.decrypt(encrypted_msg).decode()
            print(f"[CLIENT]: {message}")

            # Broadcast to other clients
            for client in clients:
                if client != client_socket:
                    client.send(encrypted_msg)

        except:
            break

    client_socket.close()
    clients.remove(client_socket)

def start():
    print("[STARTED] Server is listening...\n")

    while True:
        client_socket, addr = server.accept()
        print(f"[NEW CONNECTION] {addr}")

        clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket,)
        )
        thread.start()

start()
