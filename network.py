import socket
import json

MAX_MESSAGE_LENGTH_IN_BYTES = 4
BUFFER_SIZE = 2048


class Network:
    def __init__(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5555

    def send(self, data):
        try:
            message = json.dumps(data)
            message_length = len(message.encode('utf-8'))
            size_header = message_length.to_bytes(MAX_MESSAGE_LENGTH_IN_BYTES, byteorder='big')
            self.socket_obj.sendall(size_header + message.encode("utf-8"))
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            # Receive the length
            size_header = self.socket_obj.recv(MAX_MESSAGE_LENGTH_IN_BYTES)

            # Parse the header
            message_length = int.from_bytes(size_header[0:MAX_MESSAGE_LENGTH_IN_BYTES], byteorder='big')

            # Receive the message data
            chunks = []
            bytes_recd = 0
            while bytes_recd < message_length:
                chunk = self.socket_obj.recv(min(message_length - bytes_recd,
                                      BUFFER_SIZE))
                if not chunk:
                    raise RuntimeError("ERROR")
                chunks.append(chunk)
                bytes_recd += len(chunk)

            encoded_message = b"".join(chunks)
            test_dict = json.loads(encoded_message.decode("utf-8"))
            return test_dict
        except json.decoder.JSONDecodeError as e:
            print("JSONDecodeError: ")
            print(e)
        except ConnectionResetError as error:
            input('Check for error manually, '
                  'input anything to continue with the ConnectionResetError [WinError 10054]')
        except ConnectionAbortedError as error:
            input('Check for error manually, '
                  'input anything to continue with the ConnectionAbortedError [WinError 10053]')

    def close(self):
        self.socket_obj.close()


class ClientNetwork(Network):
    def __init__(self, server_IP):
        super().__init__()
        self.server_IP = server_IP
        self.server_addr = (self.server_IP, self.port)

    def connect(self):
        try:
            self.socket_obj.connect(self.server_addr)
        except socket.error as e:
            print(e)


class SocketToClient(Network):
    def __init__(self, socket_to_client, client_addr, client_number):
        super().__init__()
        self.socket_obj = socket_to_client
        self.client_addr = client_addr
        self.client_number = client_number


class SocketsToClients:
    def __init__(self):
        self.all_sockets_to_clients = []
        self.n_clients = 0

    def add_socket(self, new_socket: SocketToClient):
        self.all_sockets_to_clients.append(new_socket)
        self.n_clients = len(self.all_sockets_to_clients)

    def send_to_a_client(self, client_number, data):
        self.all_sockets_to_clients[client_number].send(data)

    def receive_from_a_client(self, client_number):
        return self.all_sockets_to_clients[client_number].receive()

    def send_personal_message_to_each_client(self, header, content: list):
        for client in range(self.n_clients):
            self.all_sockets_to_clients[client].send({"header": header, "content": content[client]})

    def send_same_message_to_each_client(self, header, content):
        bla = []
        for client in range(self.n_clients):
            bla.append({"header": header, "content": content})
            self.all_sockets_to_clients[client].send({"header": header, "content": content})


class ServerNetwork(Network):
    def __init__(self):
        super().__init__()
        self.server_IP = socket.gethostbyname(socket.gethostname())  # local IP address "192.168.1.109"

    def establish_connections(self, n_clients) -> SocketsToClients:
        try:
            self.socket_obj.bind((self.server_IP, self.port))
        except socket.error as e:
            str(e)

        self.socket_obj.listen(n_clients)
        print("IP is " + str(self.server_IP) + ", port: " + str(self.port))
        print("Waiting for a connection, Server Started")

        sockets_to_clients = [None] * n_clients
        sockets_to_clients = SocketsToClients()
        for client in range(0, n_clients):
            conn, addr = self.socket_obj.accept()
            print("Connected to:", addr)
            sockets_to_clients.add_socket(
                SocketToClient(socket_to_client=conn, client_addr=addr, client_number=client))
        return sockets_to_clients
