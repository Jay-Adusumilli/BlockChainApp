import socket

def handle_client(client_socket, address, clients):
    # Save client's message in variable
    message = client_socket.recv(1024).decode()

    # Extract username from message
    username = message.split()[0]

    if username in clients:
        # If the client is already in dict, update entry
        clients[username]['address'] = address
        clients[username]['message'] = message
    else:
        # Otherwise, add entry
        clients[username] = {'address': address, 'message': message}

    # Send a response
    response = 'Key updated'
    client_socket.send(response.encode())

    # TEMP! Remove this after testing
    print('Connected clients:', clients)

def start_server(host, port):

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket
    server_socket.bind((host, port))

    # Set socket to allow 5 connections
    server_socket.listen(5)

    # Empty dictionary for saving client ip's and keys
    clients = {}

    print('Server started, listening on', (host, port))

    while True:

        # Wait for a connection
        client_socket, address = server_socket.accept()

		# TEMP: remove after testing
        print("Got a connection from " + str(address[0]))	

        # Handle client's request
        handle_client(client_socket, address, clients)

        # Close client socket
        client_socket.close()

# This should be unhardcoded from localhost
# We should be using GENI machine IP
if __name__ == '__main__':
    start_server('localhost', 12345)

