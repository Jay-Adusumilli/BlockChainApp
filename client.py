import socket
import sys
import json
import random
import os.path

def send_setup_message(username, public_key):
    message = {
        "type": "setup",
        "username": username,
        "public_key": public_key
    }
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 4400))
        s.sendall(json.dumps(message).encode())
        response = s.recv(1024).decode()
        print response
        s.close()
        return True
    except Exception as e:
        print "Error connecting to server:", e
        return False

if len(sys.argv) == 2:
    if os.path.isfile('username.txt'):
        with open('username.txt', 'r') as f:
            username = f.readline().strip()
    else:
        public_key = random.randint(1, 100)
        username = "user" + str(random.randint(1, 100))
        with open('username.txt', 'w') as f:
            f.write(username)
        if send_setup_message(username, public_key):
            print "Setup successful"
        else:
            print "Setup failed"

    message = sys.argv[1]
    print "Sending message:", message, "as", username
    # TODO: send forward message to server with the given message
elif len(sys.argv) == 3 and sys.argv[1] == "directory":
    # TODO: send directory message to server and print the response
    pass
else:
    if os.path.isfile('username.txt'):
        with open('username.txt', 'r') as f:
            username = f.readline().strip()
    else:
        public_key = random.randint(1, 100)
        username = "user" + str(random.randint(1, 100))
        with open('username.txt', 'w') as f:
            f.write(username)
        if send_setup_message(username, public_key):
            print "Setup successful"
        else:
            print "Setup failed"

    print "Username:", username
    print "Public key:", public_key

def send_directory_message():
    message = {
        "type": "directory"
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', 4400))
    except Exception as e:
        print "Error connecting to server:", e
        return False

    message_str = json.dumps(message)
    s.sendall(message_str.encode())

    response = s.recv(1024).decode()
    print "Server response:", response
    s.close()
    return True


def send_forward_message(username, message):
    message = {
        "type": "forward",
        "username": username,
        "message": message
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', 4400))
    except Exception as e:
        print "Error connecting to server:", e
        return False

    message_str = json.dumps(message)
    s.sendall(message_str.encode())

    response = s.recv(1024).decode()
    print "Server response:", response
    s.close()
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python client.py <message>"
        sys.exit()

    username = "user" + str(random.randint(1, 100))
    public_key = random.randint(1, 100)

    print "Username:", username
    print "Public key:", public_key

    message_type = sys.argv[1]

    if message_type == "setup":
        if send_setup_message(username, public_key):
            with open('username.txt', 'w') as f:
                f.write(username)
    elif message_type == "directory":
        with open('username.txt', 'r') as f:
            username = f.readline().strip()

        send_directory_message(username)
    elif message_type == "forward":
        with open('username.txt', 'r') as f:
            username = f.readline().strip()

        message = " ".join(sys.argv[2:])
        send_forward_message(username, message)
    else:
        print "Invalid message type. Valid message types are 'setup', 'directory', and 'forward'"
        sys.exit()
