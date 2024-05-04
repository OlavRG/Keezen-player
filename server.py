import socket
import _thread
import json
from parse_board_state import create_starting_board_state

def read_pos(position):
    position = position.split(",")
    return int(position[0]), int(position[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def threaded_client(conn, player):
    pos = [(0, 0), (100, 100)]
    pos_serialized = json.dumps(pos[player]).encode("utf-8")
    conn.send(pos_serialized)
    reply = ""
    while True:
        try:
            data = json.loads(conn.recv(2048).decode("utf-8"))
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(json.dumps(reply).encode("utf-8"))
        except:
            break

    print("Lost connection")
    conn.close()


def establish_connections(n_clients):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_IP = socket.gethostbyname(socket.gethostname())  # local IP address "192.168.1.109"
        port = 5555

        try:
            s.bind((server_IP, port))
        except socket.error as e:
            str(e)

        s.listen(2)
        print("IP is " + str(server_IP) + ", port: " + str(port))
        print("Waiting for a connection, Server Started")

        client_sockets = [None] * n_clients
        for client in range(0, n_clients):
            conn, addr = s.accept()
            print("Connected to:", addr)
            client_sockets[client] = (conn, addr, client)
        return client_sockets

n_clients = 2
client_sockets = establish_connections(n_clients)
board_states_start = create_starting_board_state(n_clients)

for client in n_clients:
    board_states_start_serialized = json.dumps(board_states_start[client]).encode("utf-8")
    client_sockets[client][0].sendall(board_states_start_serialized)
    client_move = json.loads(client_sockets[client][0].recv(2048).decode("utf-8"))
    bla = 0

"""
    currentPlayer = 0
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        _thread.start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
"""