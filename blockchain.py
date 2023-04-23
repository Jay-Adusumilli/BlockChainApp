# Blockchain API.
import hashlib
import json

class User:
    def __init__(self, id, public_key):
        self.id = id
        self.public_key = public_key

class selfUser():
    def __init__(self, id, private_key):
        self.id = id
        self.private_key = private_key


# Class that defines a message in the blockchain.
# Takes in the hash for the last message and a list of data to add to the block.
class MsgBlock:
    def __init__(self, previous_block_hash, msg_data):

        self.previous_block_hash = previous_block_hash
        self.msg_data = msg_data

        self.block_data = f"{' - '.join(msg_data)} - {previous_block_hash}"
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

# Class that defines the blockchain as a list of blocks.
class Blockchain:
    # Initialize the blockchain with a genesis block.
    def __init__(self, user1, user2, load = False):
        # Initialize the list that holds the blocks.
        self.chain = []
        self.user1 = user1
        self.user2 = user2
        
        if load is not False:
            filename = "MessageData\\" + str(self.user1) + "_" + str(self.user2) + ".json"
            print("Loading blockchain from file...")
            self.user1 = filename.split('_')[0]
            self.user2 = filename.split('_')[1].split('.')[0]
            with open(filename, 'r') as f:
                for line in f:
                    temp = json.loads(line)
                    self.chain.append(MsgBlock(temp['previous_block_hash'], temp['msg_data']))
            return
        # If 2 users are passed in, create a new blockchain.
        elif user1 is not None and user2 is not None:
            print("Creating new blockchain...")
            self.generate_genesis_block()
            return
        # If invalid arguments are passed in, raise an exception.
        else:
            raise Exception("Invalid arguments passed to Blockchain constructor.")

    # Create the first block with a hash of 0.
    def generate_genesis_block(self):
        self.chain.append(MsgBlock("0", ["Genesis Block"]))

    # Takes in a message and creates a block from it.
    def create_block_from_transaction(self, msg_data):
        previous_block_hash = self.last_block.block_hash
        self.chain.append(MsgBlock(previous_block_hash, msg_data))
        self.write_chain()

    # Display the blockchain.
    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")

    # Write the blockchain to a file in the MessageData folder.
    def write_chain(self):
        # Create the filename.
        filename = "MessageData\\" + str(self.user1) + "_" + str(self.user2) + ".json"
        # Write the blockchain to the file.
        with open(filename, 'w') as f:
            for block in self.chain:
                json.dump(block.__dict__, f)
                f.write('\n')

    # Validate the blockchain.
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            previous = self.chain[i].previous_block_hash
            current = self.chain[i - 1].block_hash
            if previous != current:
                return False
        return True

    @property
    def last_block(self):
        return self.chain[-1]