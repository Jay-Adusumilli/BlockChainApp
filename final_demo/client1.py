import socket
import sys
from blockchain import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

SERVER_PORT = 12345
usernaem = "client1"
clients = ["client2", "client3", "client4"]


class client:
    def __init__(self, private_key, public_key):
        print("Starting client...")
        self.client_sockets = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", SERVER_PORT))
        print("Client connected.")

    def send_message(self, message):
        # Send message
        self.socket.send(message.encode())

    def receive_response(self,client_socket):
        # Receive response
        response = client_socket.recv(1024).decode()

        return response
    
    def close_socket(self, socket):
        # Close socket
        socket.close()

    def run(self):
        while True:
            try:
                pass
            except KeyboardInterrupt:
                print("Closing client...")
                sys.exit()





if __name__ == "__main__":
    client = client(1,2)
    client.run()

