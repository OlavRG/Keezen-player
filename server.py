import _thread
import json
from board_state_logic import create_starting_game_objects
from board_state_logic import create_board_states_per_client
from board_state_logic import set_pawns_to_current_player_PoV
from card_play_logic import test_all_possible_plays
from card_play_logic import card_play_to_dict
from card_play_logic import resolve_a_legal_card_play
from card_play_logic import move_card_from_hand_to_discard_and_mark_in_player_card_history
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
    players, deck, discard_pile, game_info = create_starting_game_objects(n_clients)
    board_states = create_board_states_per_client(players, deck, game_info)
    all_pawns_of_current_player_are_in_finish = False

    hands = []
    for player in players:
        hands.append(player.hand)
    while any(hands):
        # turns for each client
        for client in range(n_clients):
            sockets_to_clients[client].send(board_states[client])
            client_card_play_dict = sockets_to_clients[client].receive()

            # Define other_pawns and set pawn.position to the position from the current players POV
            other_pawns = set_pawns_to_current_player_PoV(players, players[client], game_info)

            print(players[client].color + ' hand: ' + ''.join(card.rank for card in players[client].hand))
            print('client card play: ', client_card_play_dict)

            # Make a list of all possible plays and check if the clients move is in it
            all_card_plays = test_all_possible_plays(players[client], players[client].pawns, other_pawns, players[client].hand, game_info)
            legal_card_plays = [card_play for card_play in all_card_plays if card_play[-1]["card_play_is_legal"]]
            legal_card_play_dicts = list(map(card_play_to_dict, legal_card_plays))
            if not legal_card_play_dicts:
                # Discard hand
                discard_pile.append(players[client].hand)
                players[client].cards_played_this_round += ''.join(card.rank for card in players[client].hand)
                players[client].hand[:] = []
                print('No legal card play available, hand is discarded')
            elif client_card_play_dict not in legal_card_play_dicts:
                # Play the lowest value card_play
                legal_card_play_board_values = [card_play[0]["board_value"] for card_play in legal_card_plays]
                client_card_play_index = legal_card_play_board_values.index(min(legal_card_play_board_values))
                client_card_play = legal_card_plays[client_card_play_index][0]
                resolve_a_legal_card_play(players[client], other_pawns, discard_pile, game_info, client_card_play)
                print('Provided card play is illegal. Worst card play was played instead.')
            else:
                # Print that the play is deemed legal
                print('card play is legal')
                # resolve client_card_play
                client_card_play_index = legal_card_play_dicts.index(client_card_play_dict)
                client_card_play = legal_card_plays[client_card_play_index][0]
                resolve_a_legal_card_play(players[client], other_pawns, discard_pile, game_info, client_card_play)
            board_states = create_board_states_per_client(players, deck, game_info)
            all_pawns_of_current_player_are_in_finish = all([pawn.finish for pawn in players[client].pawns])
            sockets_to_clients[client].send(all_pawns_of_current_player_are_in_finish)
            if all_pawns_of_current_player_are_in_finish:
                print("player " + str(players[client].color) + ' has won')
                break
            else:
                pass

        # Next: add multiple rounds

    """
        currentPlayer = 0
        while True:
            conn, addr = s.accept()
            print("Connected to:", addr)
    
            _thread.start_new_thread(threaded_client, (conn, currentPlayer))
            currentPlayer += 1
    """