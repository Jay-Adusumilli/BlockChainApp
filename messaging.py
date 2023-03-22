# Messaging between two computers demo.

import socket
import threading

def send_message(sock):
    # Function that sends messages to another computer.
    while True:
        message = input('You: ')
        sock.sendall(message.encode())

def receive_message(sock):
    # Function that recieves messages from another computer.
    while True:
        data = sock.recv(1024)
        if not data:
            break
        message = data.decode()
        print('Other: ' + message)

# Define the IP address and port number of the receiving computer
host = '192.168.1.2'  # Replace with the IP address of the receiving computer
port = 12345  # Choose a port number

# Create a socket object and connect to the receiving computer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Start two threads to send and receive messages
send_thread = threading.Thread(target=send_message, args=(s,))
receive_thread = threading.Thread(target=receive_message, args=(s,))
send_thread.start()
receive_thread.start()

# Wait for both threads to finish
send_thread.join()
receive_thread.join()

# Close the socket
s.close()