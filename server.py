import _thread
import json
from board_state_logic import create_players_and_cards_and_pawns
from board_state_logic import parse_board_state
from board_state_logic import create_board_states_per_client
from board_state_niche_tester import board_state_walk_backwards_and_into_finish
from card_play_logic import test_all_possible_plays
from card_play_logic import card_play_to_dict
from card_play_logic import play_any_card_on_a_pawn_and_resolve_outcome
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


if __name__ == "__main__":

    # start up code
    n_clients = 2
    initial_socket = network.ServerNetwork()
    sockets_to_clients = initial_socket.establish_connections(n_clients)
    players, deck, game_info = create_players_and_cards_and_pawns(n_clients)
    board_states = create_board_states_per_client(players, deck, game_info)
    all_pawns_of_current_player_are_in_finish = False

    while not all_pawns_of_current_player_are_in_finish:
        # turns for each client
        for client in range(n_clients):
            sockets_to_clients[client].send(board_states[client])
            client_card_play_dict = sockets_to_clients[client].receive()

            # Make a list of all possible plays and check if the clients move is in it
            other_pawns = []
            list(map(other_pawns.extend, [player.pawns for player in players if player != players[client]]))
            possible_card_plays = test_all_possible_plays(players[client], players[client].pawns, other_pawns, players[client].hand, game_info)
            legal_possible_card_plays = [card_play for card_play in possible_card_plays if card_play[-1]["card_play_is_legal"]]
            legal_possible_card_play_dicts = list(map(card_play_to_dict, legal_possible_card_plays))
            if client_card_play_dict not in legal_possible_card_play_dicts:
                # Discard hand
                players[client].hand = []
            else:
                # resolve client_card_play
                client_card_play_index = legal_possible_card_play_dicts.index(client_card_play_dict)
                client_card_play = legal_possible_card_plays[client_card_play_index]
                my_other_pawns = [pawn for pawn in players[client].pawns if pawn != client_card_play["primary_pawn"]]
                play_any_card_on_a_pawn_and_resolve_outcome(card=client_card_play["card"],
                                                            my_pawn=client_card_play["primary_pawn"],
                                                            my_other_pawns=my_other_pawns,
                                                            other_pawns=other_pawns,
                                                            game_info=game_info,
                                                            card_plays_on_pawns_and_outcomes=[],
                                                            target_pawn=client_card_play["secondary_pawn"],
                                                            move_1=client_card_play["primary_move"])
            board_states = create_board_states_per_client(players, deck, game_info)
            all_pawns_of_current_player_are_in_finish = all([pawn.finish for pawn in players[client].pawns])
            sockets_to_clients[client].send(all_pawns_of_current_player_are_in_finish)
            if all_pawns_of_current_player_are_in_finish:
                print("player " + str(players[client].color) + ' has won')
                break
            else:
                pass
            bla = 0

        # next: Add logging so we can keep track of what card plays are done and what the board looks like.
        # This also helps debug if the server correctly checks legality and resolves card plays.

    """
        currentPlayer = 0
        while True:
            conn, addr = s.accept()
            print("Connected to:", addr)
    
            _thread.start_new_thread(threaded_client, (conn, currentPlayer))
            currentPlayer += 1
    """