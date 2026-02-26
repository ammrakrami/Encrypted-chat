import socket
import threading
from cryptography.fernet import Fernet

host = input("Enter server IP: ")
port = 9999

key = input("Enter shared key: ").encode()
cipher = Fernet(key)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive():
    while True:
        try:
            encrypted_msg = client.recv(1024)
            message = cipher.decrypt(encrypted_msg).decode()
            print(f"\n[RECEIVED]: {message}")
        except:
            break

def send():
    while True:
        message = input()
        encrypted_msg = cipher.encrypt(message.encode())
        client.send(encrypted_msg)

threading.Thread(target=receive).start()
threading.Thread(target=send).start()
