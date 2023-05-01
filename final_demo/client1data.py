import socket
import threading
from blockchain import *
import random
import time

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
        time.sleep(1)
        clients = ["client2", "client3", "client4"]
        num_sent = 0
        total_byte_len = 0
        start_time = time.time()
        print("Started sending")
        for i in range(100):
            print(i)
            num_sent += 1
            byte_len = random.randrange(600, 700)
            time.sleep(0.001 * byte_len)
            total_byte_len += byte_len
            message = str(random.randbytes(byte_len))
            client = random.choice(clients)
            msg = client_id + ">" + client + ":" + message
            self.blockchain_client1_client2.create_block_from_transaction(client_id, message)
            self.client_socket.sendall(msg.encode())
            self.validate_chains(True)
        
        finish_time = time.time()
        print("Finished sending\n\n")
        print("Total messages sent: " + str(num_sent))
        print("Total bytes sent: " + str(total_byte_len))
        print("Total time taken: " + str(finish_time - start_time))
        print("Average messages per second: " + str(num_sent / (finish_time - start_time)))
        print("Average bytes per second: " + str(total_byte_len / (finish_time - start_time)))
        print("Average seconds per message: " + str((finish_time - start_time) / num_sent))
        print("Average message size: " + str(total_byte_len / num_sent))




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

    random.seed()

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