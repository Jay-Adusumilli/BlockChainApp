import socket
import select


class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.client_sockets = [self.server_socket]

    def run(self):
        print(f'Server listening on port {self.port}...')

        while True:
            # Use select to find readable and writeable sockets
            read_sockets, write_sockets, error_sockets = select.select(self.client_sockets, self.client_sockets, [])

            # Process readable sockets
            for sock in read_sockets:
                if sock is self.server_socket:
                    # Accept incoming connections
                    client_socket, client_address = self.server_socket.accept()
                    print('Connection from', client_address)

                    # Add the new client socket to the list
                    self.client_sockets.append(client_socket)
                else:
                    # Receive data from the client
                    data = sock.recv(1024)
                    if data:
                        print(f'Received "{data.decode()}" from {sock.getpeername()}')

                        # Send data to all clients
                        for socket in self.client_sockets:
                            if socket is not self.server_socket and socket is not sock:
                                socket.sendall(data)
                    else:
                        # If there is an error with the socket or the client disconnects, remove the socket from the list
                        print(f'Connection closed by {sock.getpeername()}')
                        self.client_sockets.remove(sock)
                        sock.close()

            # Process writeable sockets
            for sock in write_sockets:
                pass  # TODO: Implement writing to sockets as needed

            # Process error sockets
            for sock in error_sockets:
                # If there is an error with the socket, remove it from the list
                print(f'Error with {sock.getpeername()}')
                self.client_sockets.remove(sock)
                sock.close()

if __name__ == '__main__':
    server = Server()
    server.run()