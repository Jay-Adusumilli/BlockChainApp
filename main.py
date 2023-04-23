from blockchain import *

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

# Fetch a blockchain between 2 users.
user1_user2_blockchain = Blockchain(filename="Alice_Bob.json")

# Mint the messages onto the blockchain.
#user1_user2_blockchain.create_block_from_transaction([user1id, m1]);
#user1_user2_blockchain.create_block_from_transaction([user2id, m2]);
#user1_user2_blockchain.create_block_from_transaction([user1id, m3]);
#user1_user2_blockchain.create_block_from_transaction([user2id, m4]);

# Print out the blockchain.
user1_user2_blockchain.display_chain()

# Validate the blockchain.
print(user1_user2_blockchain.validate_chain())