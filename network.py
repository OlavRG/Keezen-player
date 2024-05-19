import socket
import json


class Network:
    def __init__(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5555

    def send(self, data):
        try:
            self.socket_obj.send(json.dumps(data).encode("utf-8"))
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return json.loads(self.socket_obj.recv(2048).decode("utf-8"))
        except socket.error as e:
            print(e)

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


class ServerToClientNetwork(Network):
    def __init__(self, socket_to_client, client_addr, client_number):
        super().__init__()
        self.socket_obj = socket_to_client
        self.client_addr = client_addr
        self.client_number = client_number


class ServerNetwork(Network):
    def __init__(self):
        super().__init__()
        self.server_IP = socket.gethostbyname(socket.gethostname())  # local IP address "192.168.1.109"

    def establish_connections(self, n_clients):
        try:
            self.socket_obj.bind((self.server_IP, self.port))
        except socket.error as e:
            str(e)

        self.socket_obj.listen(2)
        print("IP is " + str(self.server_IP) + ", port: " + str(self.port))
        print("Waiting for a connection, Server Started")

        sockets_to_clients = [None] * n_clients
        for client in range(0, n_clients):
            conn, addr = self.socket_obj.accept()
            print("Connected to:", addr)
            sockets_to_clients[client] = ServerToClientNetwork(socket_to_client=conn, client_addr=addr, client_number=client)
            bla = 1
        return sockets_to_clients
