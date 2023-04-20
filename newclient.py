import socket
import sys

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Hostname is from cla
host = sys.argv[1]

# set the port number
port = 12345

# Connect to server
client_socket.connect((host, port))

# Message is from CLA
message = sys.argv[2]
client_socket.send(message.encode())

# TEMP: remove this after testing, server will not be sending response
# If it does, it won't need to be printed
response = client_socket.recv(1024).decode()
print('Received response from server: {}'.format(response))

# Close socket
client_socket.close()

