import socket
from threading import Thread
import sys

class server:
    def __init__(self):
        print("Starting server...")
        self.server_listen_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_listen_socket_1.bind(("localhost", 12345))

        self.server_listen_socket_1.listen(4)
        self.client1, self.address1 = self.server_listen_socket_1.accept()
        self.client2, self.address2 = self.server_listen_socket_1.accept()
        self.client3, self.address3 = self.server_listen_socket_1.accept()
        self.client4, self.address4 = self.server_listen_socket_1.accept()


    def run(self):
        while True:
            try:
                data1 = self.client1.recv(1024).decode()
                data2 = self.client2.recv(1024).decode()
                data3 = self.client3.recv(1024).decode()
                data4 = self.client4.recv(1024).decode()
                if data1:
                    self.client2.send(data1.encode())
                    self.client3.send(data1.encode())
                    self.client4.send(data1.encode())
                if data2:
                    self.client1.send(data2.encode())
                    self.client3.send(data2.encode())
                    self.client4.send(data2.encode())
                if data3:
                    self.client1.send(data3.encode())
                    self.client2.send(data3.encode())
                    self.client4.send(data3.encode())
                if data4:
                    self.client1.send(data4.encode())
                    self.client2.send(data4.encode())
                    self.client3.send(data4.encode())
                
            except KeyboardInterrupt:
                print("Closing server...")
                sys.exit()


if __name__ == "__main__":
    server = server()
    server.run()