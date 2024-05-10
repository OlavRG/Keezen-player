import _thread
import json
from board_state_logic import create_players_cards_and_pawns
from board_state_logic import parse_board_state
from card_play_logic import test_all_possible_plays
from card_play_logic import card_play_to_dict
import network

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


n_clients = 1
initial_socket = network.ServerNetwork()
sockets_to_clients = initial_socket.establish_connections(n_clients)
players, deck, game_info = create_players_cards_and_pawns(n_clients)

for client in range(n_clients):
    sockets_to_clients[client].send(board_states_start[client])
    client_card_play_dict = sockets_to_clients[client].receive()

    [player, my_pawns, other_pawns, hand, game_info] = parse_board_state(board_states_start[client])

    # Make a list of all possible plays and check if the clients move is in it
    possible_card_plays = test_all_possible_plays(player, my_pawns, other_pawns, hand, game_info)
    legal_possible_card_plays = [card_play for card_play in possible_card_plays if card_play[-1]["card_play_is_legal"]]
    legal_possible_card_play_dicts = list(map(card_play_to_dict, legal_possible_card_plays))
    if client_card_play_dict not in legal_possible_card_play_dicts:
        # Discard hand
        hand = []
    else:
        # resolve client_card_play
        client_card_play_index = legal_possible_card_play_dicts.index(client_card_play_dict)
        client_card_play = legal_possible_card_plays[client_card_play_index]


    bla = 0

    # next: create a functions that makes a board state per player from the player, card, and pawn objects.

"""
    currentPlayer = 0
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        _thread.start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
"""