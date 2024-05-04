import socket
import json

class Network:
    def __init__(self, server_IP):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_IP
        self.port = 5555
        self.addr = (self.server, self.port)
        self.board_state = self.connect()

    def get_board_state(self):
        return self.board_state

    def connect(self):
        try:
            self.client.connect(self.addr)
            return json.loads(self.client.recv(2048).decode("utf-8"))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode("utf-8"))
            return json.loads(self.client.recv(2048).decode("utf-8"))
        except socket.error as e:
            print(e)
