import socket
import threading
from blockchain import *

client_number = 1
client_id = "client" + str(client_number)


class Client:
    def __init__(self, userlist, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Create a blockchain for each client connection.
        self.blockchain_client1_client2 = Blockchain("client1", "client2", userlist)
        self.blockchain_client1_client3 = Blockchain("client1", "client3", userlist)
        self.blockchain_client1_client4 = Blockchain("client1", "client4", userlist)
        self.blockchain_client2_client3 = Blockchain("client2", "client1", userlist)
        self.blockchain_client2_client4 = Blockchain("client2", "client4", userlist)
        self.blockchain_client3_client4 = Blockchain("client3", "client4", userlist)


    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print('Connected to server')

    def send_messages(self):
        while True:
            message = input('Enter a message > ')
            client = input('Select a client > ')
            select_corrupt = input('Corrupt message? (y/n) > ')
            if client == "client2":
                message = client_id + ">" + "client2" + ":" + message
                if select_corrupt == "y":
                    message = "corrupt" + message
                self.blockchain_client1_client2.add_new_transaction(message)
                self.client_socket.sendall(message.encode())
            elif client == "client3":
                message = client_id + ">" + "client3" + ":" + message
                self.blockchain_client1_client3.add_new_transaction(message)
                self.client_socket.sendall(message.encode())
            elif client == "client4":
                message = client_id + ">" + "client4" + ":" + message
                self.blockchain_client1_client4.add_new_transaction(message)
                self.client_socket.sendall(message.encode())
            else:
                print("Invalid client")
                continue

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(1024).decode()
            print(f'Received "{message}"')
            message_author = message.split(":")[0]
            message_content = message.split(":")[1]
            if message_author == "client2":
                self.

    def run(self):
        self.connect()

        send_thread = threading.Thread(target=self.send_messages)
        receive_thread = threading.Thread(target=self.receive_messages)

        send_thread.start()
        receive_thread.start()

        send_thread.join()
        receive_thread.join()

        self.client_socket.close()

if __name__ == '__main__':

    # Read all public and private keys from files:
    # 1
    with open('keys\\private1.pem', 'rb') as f:
        private_key_1 = RSA.import_key(f.read())
    with open('keys\\public1.pem', 'rb') as f:
        public_key_1 = RSA.import_key(f.read())
    # 2
    with open('keys\\private2.pem', 'rb') as f:
        private_key_2 = RSA.import_key(f.read())
    with open('keys\\public2.pem', 'rb') as f:
        public_key_2 = RSA.import_key(f.read())
    # 3
    with open('keys\\private3.pem', 'rb') as f:
        private_key_3 = RSA.import_key(f.read())
    with open('keys\\public3.pem', 'rb') as f:
        public_key_3 = RSA.import_key(f.read())
    # 4
    with open('keys\\private4.pem', 'rb') as f:
        private_key_4 = RSA.import_key(f.read())
    with open('keys\\public4.pem', 'rb') as f:
        public_key_4 = RSA.import_key(f.read())

    user_private_key = private_key_1

    # Create userlist
    userlist = UserList(client_id, user_private_key)
    userlist.add_user("client2", public_key_2)
    userlist.add_user("client3", public_key_3)
    userlist.add_user("client4", public_key_4)




    client = Client(userlist)
    client.run()