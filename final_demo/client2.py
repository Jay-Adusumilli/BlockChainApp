import socket
import threading
from blockchain import *

client_number = 2
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

    def validate_chains(self, send):
        c1c2, c1c2hash = self.blockchain_client1_client2.validate_chain()
        c1c3, c1c3hash = self.blockchain_client1_client3.validate_chain()
        c1c4, c1c4hash = self.blockchain_client1_client4.validate_chain()
        c2c3, c2c3hash = self.blockchain_client2_client3.validate_chain()
        c2c4, c2c4hash = self.blockchain_client2_client4.validate_chain()
        c3c4, c3c4hash = self.blockchain_client3_client4.validate_chain()
        if c1c2 and c1c3 and c1c4 and c2c3 and c2c4 and c3c4:
            print("All blockchains are valid, sending...")
            hashes = [c1c2hash, c1c3hash, c1c4hash, c2c3hash, c2c4hash, c3c4hash]
            temp = hashes
            hashes = "validate:" + " ".join(hashes)
            if send:
                self.client_socket.sendall(hashes.encode())
        elif not c1c2:
            print("Blockchain between client1 and client2 is invalid")
        elif not c1c3:
            print("Blockchain between client1 and client3 is invalid")
        elif not c1c4:
            print("Blockchain between client1 and client4 is invalid")
        elif not c2c3:
            print("Blockchain between client2 and client3 is invalid")
        elif not c2c4:
            print("Blockchain between client2 and client4 is invalid")
        elif not c3c4:
            print("Blockchain between client3 and client4 is invalid")
        return temp

    def display_blockchains(self):
        print("--Client1 to Client2--")
        self.blockchain_client1_client2.display_chain()
        print("--Client1 to Client3--")
        self.blockchain_client1_client3.display_chain()
        print("--Client1 to Client4--")
        self.blockchain_client1_client4.display_chain()
        print("--Client2 to Client3--")
        self.blockchain_client2_client3.display_chain()
        print("--Client2 to Client4--")
        self.blockchain_client2_client4.display_chain()
        print("--Client3 to Client4--")
        self.blockchain_client3_client4.display_chain()

    def send_messages(self):
        while True:
            command = input('Enter a command > ')
            if command == "quit":
                self.client_socket.close()
                break
            elif command == "validate":
                x = self.validate_chains(True)
                #print(x)
                continue
            elif command == "view":
                self.display_blockchains()
            elif command == "mal_msg":
                message = input('Enter a message to send > ')
                client = input('Select a client > ')
                if client == "client1":
                    msg = client_id + ">" + "client1" + ":" + message
                    message = input("Enter a message to add to blockchain > ")
                    self.blockchain_client1_client2.create_block_from_transaction(client_id, message)
                    self.client_socket.sendall(msg.encode())
                elif client == "client3":
                    msg = client_id + ">" + "client3" + ":" + message
                    message = input("Enter a message to add to blockchain > ")
                    self.blockchain_client1_client3.create_block_from_transaction(client_id, message)
                    self.client_socket.sendall(msg.encode())
                elif client == "client4":
                    msg = client_id + ">" + "client4" + ":" + message
                    message = input("Enter a message to add to blockchain > ")
                    self.blockchain_client1_client4.create_block_from_transaction(client_id, message)
                    self.client_socket.sendall(msg.encode())
                else:
                    print("Invalid client")
                    continue
            elif command == "msg":
                message = input('Enter a message > ')
                client = input('Select a client > ')
                if client == "client1":
                    msg = client_id + ">" + "client1" + ":" + message
                    self.blockchain_client1_client2.create_block_from_transaction(client_id, message)
                    self.client_socket.sendall(msg.encode())
                elif client == "client3":
                    msg = client_id + ">" + "client3" + ":" + message
                    self.blockchain_client1_client3.create_block_from_transaction(client_id, message)
                    self.client_socket.sendall(msg.encode())
                elif client == "client4":
                    msg = client_id + ">" + "client4" + ":" + message
                    self.blockchain_client1_client4.create_block_from_transaction(client_id, message)
                    self.client_socket.sendall(msg.encode())
                else:
                    print("Invalid client")
                    continue

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(10000).decode()
            print(f'\nReceived "{message}"')
            message_authors = message.split(":")[0]
            message_content = message.split(":")[1]
            if message_authors == "validate":
                hashes = self.validate_chains(False)
                input = message.split(":")[1].split(" ")
                #print(hashes, input)
                valid = True
                print("Validating blockchains...")
                for i in range(len(hashes)):
                    if hashes[i] != input[i]:
                        valid = False
                        print("Blockchain at " + str(hashes[i]) + " did not match " + str(input[i] + "..."))
                        break
                continue
            message_author1 = message_authors.split(">")[0]
            message_author2 = message_authors.split(">")[1]
            if message_author1 == "client2" and message_author2 == "client3":
                self.blockchain_client2_client3.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client2" and message_author2 == "client4":
                self.blockchain_client2_client4.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client3" and message_author2 == "client4":
                self.blockchain_client3_client4.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client3" and message_author2 == "client2":
                self.blockchain_client2_client3.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client4" and message_author2 == "client2":
                self.blockchain_client2_client4.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client4" and message_author2 == "client3":
                self.blockchain_client3_client4.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client1" and message_author2 == "client2":
                self.blockchain_client1_client2.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client1" and message_author2 == "client3":
                self.blockchain_client1_client3.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client1" and message_author2 == "client4":
                self.blockchain_client1_client4.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client2" and message_author2 == "client1":
                self.blockchain_client1_client2.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client3" and message_author2 == "client1":
                self.blockchain_client1_client3.create_block_from_transaction(message_author1, message_content)
            elif message_author1 == "client4" and message_author2 == "client1":
                self.blockchain_client1_client4.create_block_from_transaction(message_author1, message_content)
            else:
                print("Invalid message")
            

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

    user_private_key = private_key_2

    # Create userlist
    userlist = UserList(client_id, user_private_key)
    userlist.add_user("client1", public_key_1)
    userlist.add_user("client3", public_key_3)
    userlist.add_user("client4", public_key_4)




    client = Client(userlist)
    client.run()