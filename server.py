import socket
import json

# Dictionary to store registered clients
clients = {}

# Function to handle setup messages from clients
def handle_setup(message, address):
    global clients
    username = message['username']
    public_key = message['public_key']

    if username in clients:
        # If the client is already in the dictionary, update their entry
        clients[username]['address'] = address
        clients[username]['public_key'] = public_key
    else:
        # Otherwise, add a new entry for the client
        clients[username] = {'address': address, 'public_key': public_key}

    # Send a response to the client
    response = {'status': 'success'}
    return response

# Function to handle directory messages from clients
def handle_directory():
    global clients
    users = list(clients.keys())
    response = {'status': 'success', 'users': users}
    return response

# Function to handle forward messages from clients
def handle_forward(message):
    global clients
    recipient = message['recipient']
    message_text = message['message']

    if recipient in clients:
        # If the recipient is in the dictionary, forward the message to them
        recipient_address = clients[recipient]['address']
        sender = message['sender']
        forward_message = {'sender': sender, 'message': message_text}
        forward_message_str = json.dumps(forward_message).encode()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(recipient_address)
        client_socket.send(forward_message_str)
        client_socket.close()
        response = {'status': 'success'}
    else:
        # Otherwise, return an error message to the sender
        response = {'status': 'error', 'message': 'Recipient not found'}

    return response

# Function to handle client requests
def handle_client(client_socket, address):
    global clients
    # Receive message from client
    message_str = client_socket.recv(1024).decode()
    message = json.loads(message_str)

    # Handle message based on type
    message_type = message['type']
    if message_type == 'setup':
        response = handle_setup(message, address)
    elif message_type == 'directory':
        response = handle_directory()
    elif message_type == 'forward':
        sender_address = address
        sender = [k for k, v in clients.items() if v['address'] == sender_address][0]
        message['sender'] = sender
        response = handle_forward(message)
    else:
        response = {'status': 'error', 'message': 'Invalid message type'}

    # Send response to client
    response_str = json.dumps(response).encode()
    client_socket.send(response_str)

    # Close client socket
    client_socket.close()

# Function to start the server
def start_server():
    global clients
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to localhost on port 12345
    server_socket.bind(('localhost', 4400))

    # Set socket to allow 5 connections
    server_socket.listen(5)

    print('Server started')

    while True:
        # Wait for a connection
        client_socket, address = server_socket.accept()

        # Handle client request in a new thread
        handle_client(client_socket, address)

# Start the server
start_server()

