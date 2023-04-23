# Blockchain Demo.
import hashlib

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
    def __init__(self, user1 = None, user2 = None, filename = None):
        if filename is not None:
            print("Loading blockchain from file...")
            self.user1 = filename.split('_')[0]
            self.user2 = filename.split('_')[1].split('.')[0]
            with open(filename, 'r') as f:
                self.chain = json.load(f)
            return
        elif user1 is not None and user2 is not None:
            print("Creating new blockchain...")
            self.user1 = user1
            self.user2 = user2
            self.chain = []
            self.generate_genesis_block()
            return
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

    # Write the blockchain to a file.
    def write_chain(self):
        # Create the filename.
        filename = self.user1 + "_" + self.user2 + ".json"
        # Write the blockchain to the file.
        with open(filename, 'w') as f:
            for block in self.chain:
                f.write(block)

            

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

def main():
    # Start a blockchain between 2 users.
    user1id = "Alice"
    user2id = "Bob"

    # User 1 says Hello.
    m1 = "Hello"
    # User 2 says Hi.
    m2 = "Hii"
    # User 1 says Test.
    m3 = "Test"
    # User 2 says Reply.
    m4 = "Reply"

    # Create a blockchain between 2 users.
    user1_user2_blockchain = Blockchain(user1id, user2id)

    # Mint the messages onto the blockchain.
    user1_user2_blockchain.create_block_from_transaction([user1id, m1]);
    user1_user2_blockchain.create_block_from_transaction([user2id, m2]);
    user1_user2_blockchain.create_block_from_transaction([user1id, m3]);
    user1_user2_blockchain.create_block_from_transaction([user2id, m4]);

    # Print out the blockchain.
    user1_user2_blockchain.display_chain()

    # Validate the blockchain.
    print(user1_user2_blockchain.validate_chain())


if __name__ == "__main__":
    main()