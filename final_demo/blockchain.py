# Blockchain API.
import hashlib
import warnings
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# Class that defines a user list.
class UserList:
    # Initialize the user list.
    def __init__(self, selfid, private_key):
        self.id = selfid
        self.private_key = private_key
        self.user_list = {}
                
    # Add a user to the list.
    def add_user(self, id, public_key):
        self.user_list[str(id)] = public_key
            
    def isSelfUser(self, id):
        if self.id == id:
            return True
        else:
            return False

    def getPrivateKey(self):
        return self.private_key

    # Get a user from the list.
    def get_user(self, id):
        try:
            return self.user_list[str(id)]
        except:
            warnings.warn("User not found.")
            return None        

# Class that defines a message in the blockchain.
# Takes in the hash for the last message and a list of data to add to the block.
class MsgBlock:
    def __init__(self, previous_block_hash, id, msg_data):

        self.previous_block_hash = previous_block_hash
        self.msg_data = msg_data
        self.userid = id
        self.block_data = self.previous_block_hash + self.userid + "_" + self.msg_data
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

# Class that defines the blockchain as a list of blocks.
class Blockchain:
    # Initialize the blockchain with a genesis block.
    def __init__(self, user1, user2, userlist):
        # Initialize the list that holds the blocks.
        self.chain = []
        self.user1 = user1
        self.user2 = user2
        self.userlist = userlist
        # If 2 users are passed in, create a new blockchain.
        if user1 is not None and user2 is not None:
            print("Creating new blockchain...")
            self.generate_genesis_block()
            return
        # If invalid arguments are passed in, raise an exception.
        else:
            raise Exception("Invalid arguments passed to Blockchain constructor.")

    # Create the first block with a hash of 0.
    def generate_genesis_block(self):
        self.chain.append(MsgBlock("0", "0","Genesis Block"))

    # Takes in a message and creates a block from it.
    def create_block_from_transaction(self, user, msg_data):
        public_key = self.userlist.getPrivateKey()
        cipher = PKCS1_OAEP.new(public_key)
        encypted_msg = cipher.encrypt(msg_data)
        previous_block_hash = self.last_block.block_hash
        self.chain.append(MsgBlock(previous_block_hash, user, encypted_msg))

    # Decrypts the message in a block.
    def decrypt_block(self, block):
        private_key = self.userlist.getPrivateKey()
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(block.msg_data)

    # Looks in the chain to find blocks from self and decrypts them.
    def decrypt_chain(self):
        if self.userlist.isSelfUser(self.user1) or self.userlist.isSelfUser(self.user2):
            decypted_chain = []
            for i, block in enumerate(self.chain):
                if not self.userlist.isSelfUser(block.userid):
                    decypted_chain.append(self.decrypt_block(block))
                else:
                    decypted_chain.append(self.get_block_message(block))
            return decypted_chain
        else:
            warnings.warn("Cannot decrypt chain for user not in conversation.")
            return None

    # Display the blockchain.
    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")

    # Validate the blockchain.
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            previous = self.chain[i].previous_block_hash
            current = self.chain[i - 1].block_hash
            if previous != current:
                return False, self.chain[i].block_hash
        return True, self.last_block.block_hash
    
    # A mallicious user can change the data in a block.
    def change_block_data(self, block_number, new_data):
        self.chain[block_number].msg_data = new_data
        self.chain[block_number].block_data = self.chain[block_number].previous_block_hash + self.chain[block_number].userid + "_" + self.chain[block_number].msg_data
        self.chain[block_number].block_hash = hashlib.sha256(self.chain[block_number].block_data.encode()).hexdigest()

    # Get the last block in the chain.
    @property
    def last_block(self):
        return self.chain[-1]





