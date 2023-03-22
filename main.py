### Main Python File
import hashlib

class MsgBlock:
    
    def __init__(self, previous_block_hash, transaction_list):

        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash}"
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()



class Blockchain:
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        self.chain.append(MsgBlock("0", ["Genesis Block"]))

    def create_block_from_transaction(self, transaction_list):
        previous_block_hash = self.last_block.block_hash
        self.chain.append(MsgBlock(previous_block_hash, transaction_list))

    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")

    @property
    def last_block(self):
        return self.chain[-1]


# Start a blockchain between 2 users.
user1id = "Alice"
user2id = "Bob"

# User 1 says Hello.
m1 = "Hello"
# User 2 says Hi.
m2 = "Hi"
# User 1 says Test.
m3 = "Test"
# User 2 says Reply.
m4 = "Reply"

# Create a blockchain between 2 users.
user1_user2_blockchain = Blockchain()

# Mint the messages onto the blockchain.
user1_user2_blockchain.create_block_from_transaction([user1id, m1]);
user1_user2_blockchain.create_block_from_transaction([user2id, m2]);
user1_user2_blockchain.create_block_from_transaction([user1id, m3]);
user1_user2_blockchain.create_block_from_transaction([user2id, m4]);

# Print out the blockchain.
user1_user2_blockchain.display_chain()
