import socket
import threading
import json

def handle_incoming_messages(client_socket):
    buffer = b''  # buffer to store received data
    while True:
        # Receive message from server
        data = client_socket.recv(1024)
        if not data:
            break
        buffer += data

        # Split buffer into individual messages
        messages = buffer.split(b'\n')

        # Process each complete message
        for message in messages[:-1]:
            message_str = message.decode()
            message = json.loads(message_str)

            # Handle message based on type
            message_type = message['type']
            if message_type == 'forward':
                sender = message['sender']
                message_text = message['message']
                print(f"Received message from {sender}: {message_text}")
            elif message_type == 'error':
                print(f"Error: {message['message']}")
            else:
                print(f"Invalid message type: {message_type}")

        # Store any remaining partial message in buffer
        buffer = messages[-1]

# Function to send a forward message
def send_forward_message(client_socket, recipient, message_text):
    # Construct message
    message = {'type': 'forward', 'recipient': recipient, 'message': message_text}
    message_str = json.dumps(message).encode()

    # Send message to server
    client_socket.send(message_str)

# Function to send a directory message
def send_directory_message(client_socket):
    # Construct message
    message = {'type': 'directory'}
    message_str = json.dumps(message).encode()

    # Send message to server
    client_socket.send(message_str)

    # Receive response from server
    response_str = client_socket.recv(1024).decode()
    response = json.loads(response_str)

    # Handle response
    if response['status'] == 'success':
        users = response['users']
        print("Registered users:")
        for user in users:
            print(user)
    else:
        print(f"Error: {response['message']}")

# Function to handle client actions
def handle_client():
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    server_address = ('localhost', 4400)
    client_socket.connect(server_address)

    # Start thread to handle incoming messages
    incoming_thread = threading.Thread(target=handle_incoming_messages, args=(client_socket,))
    incoming_thread.start()

    # Get username and public key from user
    username = input("Enter your username: ")
    public_key = input("Enter your public key: ")

    # Send setup message to server
    message = {'type': 'setup', 'username': username, 'public_key': public_key}
    message_str = json.dumps(message).encode()
    client_socket.send(message_str)

    # Receive response from server
    response_str = client_socket.recv(1024).decode()
    response = json.loads(response_str)

    # Handle response
    if response['status'] == 'success':
        print(f"Connected to server as {username}")
    else:
        print(f"Error: {response['message']}")
        return

    # Loop to handle user input
    while True:
        action = input("Enter an action (send, directory, quit): ")
        if action == 'send':
            recipient = input("Enter recipient username: ")
            message_text = input("Enter message: ")
            send_forward_message(client_socket, recipient, message_text)
        elif action == 'directory':
            send_directory_message(client_socket)
        elif action == 'quit':
            client_socket.close()
            return
        else:
            print("Invalid action")

# Start the client
handle_client()

