import _thread
import json
import random
import network
import server_logging
from board_state_logic import create_starting_game_objects
from board_state_logic import create_board_states_per_client
from board_state_logic import set_pawns_to_current_player_PoV
from board_state_logic import deal_cards_from_deck_to_players
from card_play_logic import test_all_possible_plays
from card_play_logic import card_play_to_dict
from card_play_logic import do_card_play_and_resolve_outcome
from card_play_logic import move_card_from_hand_to_discard_and_mark_in_player_card_history
from client_view import print_player_view


if __name__ == "__main__":

    # start up code
    logger = server_logging.create_logger()
    n_clients = int(input("How many players are joining? Please state a number <9"))  # limit by create_starting_game_ob
    initial_socket = network.ServerNetwork()
    sockets_to_clients = initial_socket.establish_connections(n_clients)
    players, deck, discard_pile, game_info = create_starting_game_objects(n_clients)
    all_pawns_of_current_player_are_in_finish = False

    hands = []
    for player in players:
        hands.append(player.hand)

    while not all_pawns_of_current_player_are_in_finish:
        # reset the deck when all cards are in the discard pile
        if len(deck) == 0 and len(discard_pile) != 0:
            deck.extend(discard_pile[:])
            random.shuffle(deck)
            discard_pile[:] = []
        else:
            pass
        while deck:
            if len(deck) == 13 * game_info.player_count:
                deal_cards_from_deck_to_players(players, deck, 5)
            elif len(deck) < (13 * game_info.player_count) and len(deck) % 4 == 0:
                deal_cards_from_deck_to_players(players, deck, 4)
            else:
                raise Exception(f"Unexpected deck size. Deck is either greater than 13*players, or not dividable by 4."
                                f"{len(deck)=}")
            board_states = create_board_states_per_client(players, deck, game_info)

            while any(hands):
                # turns for each client
                for client in range(n_clients):
                    # Update current player in board state
                    for board_state in board_states:
                        board_state["current_player_color"] = players[client].color

                    # Send board state and cards in hand to all players at start of each turn
                    network.send_personal_message_to_each_client(sockets_to_clients, n_clients, 'view_board_state',
                                                                 board_states)
                    # Ask current player to make a move
                    sockets_to_clients[client].send({"header": 'play_from_board_state',
                                                     "content": board_states[client]})
                    client_card_play_dict = sockets_to_clients[client].receive()
                    logger.info(client_card_play_dict)

                    # Define other_pawns and set pawn.position to the position from the current players POV
                    other_pawns = set_pawns_to_current_player_PoV(players, players[client], game_info)
                    current_player_color = players[client].color

                    print_player_view(players[client], current_player_color, other_pawns, game_info)

                    print('client card play: ', client_card_play_dict)

                    # Make a list of all possible plays and check if the clients move is in it
                    all_card_plays = test_all_possible_plays(players[client], other_pawns, discard_pile, game_info)
                    legal_card_plays = [card_play for card_play in all_card_plays if card_play[-1]["card_play_is_legal"]]
                    legal_card_play_dicts = list(map(card_play_to_dict, legal_card_plays))
                    if not legal_card_play_dicts:
                        print('No legal card play available')
                        # Discard hand
                        if players[client].hand:
                            discard_pile.extend(players[client].hand[:])
                            players[client].card_history += ''.join(card.rank for card in players[client].hand)
                            players[client].hand[:] = []
                            print('No legal card play available, hand is discarded')
                        else:
                            print('No legal card play available')
                    elif client_card_play_dict not in legal_card_play_dicts:
                        # Play the lowest value card_play
                        legal_card_play_board_values = [card_play[0]["board_value"] for card_play in legal_card_plays]
                        worst_card_play_index = legal_card_play_board_values.index(min(legal_card_play_board_values))
                        worst_card_play = legal_card_plays[worst_card_play_index][0]
                        print('Provided card play is illegal. Worst card play was played instead.')
                        print('Substituted card play: ', card_play_to_dict([worst_card_play]))
                        do_card_play_and_resolve_outcome(worst_card_play, players[client], other_pawns, game_info,
                                                         card_plays_on_pawns_and_outcomes=[])
                        # Discard card from hand
                        move_card_from_hand_to_discard_and_mark_in_player_card_history(players[client],
                                                                                       worst_card_play["card"],
                                                                                       discard_pile)
                    else:
                        # Print that the play is deemed legal
                        print('card play is legal')
                        # resolve client_card_play
                        client_card_play_index = legal_card_play_dicts.index(client_card_play_dict)
                        client_card_play = legal_card_plays[client_card_play_index][0]
                        do_card_play_and_resolve_outcome(client_card_play, players[client], other_pawns, game_info,
                                                         card_plays_on_pawns_and_outcomes=[])
                        # Discard card from hand
                        move_card_from_hand_to_discard_and_mark_in_player_card_history(players[client],
                                                                                       client_card_play["card"],
                                                                                       discard_pile)
                    board_states = create_board_states_per_client(players, deck, game_info)
                    all_pawns_of_current_player_are_in_finish = all([pawn.finish for pawn in players[client].pawns])
                    print("before send all pawns")
                    network.send_same_message_to_each_client(sockets_to_clients, n_clients,
                                                             'all_pawns_of_current_player_are_in_finish',
                                                             all_pawns_of_current_player_are_in_finish)
                    if all_pawns_of_current_player_are_in_finish:
                        print("player " + str(players[client].color) + ' has won')
                        break
                if all_pawns_of_current_player_are_in_finish:
                    break
            if all_pawns_of_current_player_are_in_finish:
                break
        if all_pawns_of_current_player_are_in_finish:
            break
    print("game successfully finished")
    input("Type anything to close server")

    # NExt: keep debugging server while playing to find why some plays are marked illegal.
    # Issue1: player input for pawns and cards are not always properly processed. Other cards in hand are played on
    # other pawns instead. --> this seems to be an issue where the server interprets a card play as illegal.

    # Next: Also add a results screen at the end of a game where the end state is reported to all players.
    # Next: define all card_play_logic input and output in terms of game objects and card_play
    # Next: play
