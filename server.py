import _thread
import json
import random
import network
import server_logging
from board_state_logic import create_starting_game_objects
from board_state_logic import move_cards_from_discard_to_deck_and_shuffle
from board_state_logic import create_board_states_per_client
from board_state_logic import deal_cards_from_deck_to_players
from card_play_logic import test_all_possible_plays
from card_play_logic import card_play_to_dict
from card_play_logic import do_card_play_and_resolve_outcome
from card_play_logic import move_card_from_hand_to_discard_and_mark_in_player_card_history
from card_play_logic import is_card_play_legal
from card_play_logic import card_play_dict_to_card_play
from client_view import print_player_view
from server_CLI_view import how_many_players_in_game, view_client_card_play


if __name__ == "__main__":

    # start up code
    logger = server_logging.create_logger()
    n_clients = how_many_players_in_game()
    initial_socket = network.ServerNetwork()
    sockets_to_clients = initial_socket.establish_connections(n_clients)
    players, deck, discard_pile, game_info = create_starting_game_objects(n_clients)
    all_pawns_of_current_player_are_in_finish = False

    while not all_pawns_of_current_player_are_in_finish:
        # reset the deck when all cards are in the discard pile
        move_cards_from_discard_to_deck_and_shuffle(deck, discard_pile)
        while deck:
            deal_cards_from_deck_to_players(players, deck, game_info)
            board_states = create_board_states_per_client(players, deck, game_info)

            while any([player.hand for player in players]):
                # turns for each client
                for player_index, current_player in enumerate(players):
                    # Update current player in board state
                    for board_state in board_states:
                        board_state["current_player_color"] = current_player.color

                    # Send board state and cards in hand to all players at start of each turn
                    sockets_to_clients.send_personal_message_to_each_client('view_board_state',
                                                                            board_states)
                    # Ask current player to make a move
                    sockets_to_clients.send_to_a_client(player_index, 'play_from_board_state', board_states[player_index])
                    client_card_play_dict = sockets_to_clients.receive_from_a_client(player_index)
                    logger.info(client_card_play_dict)

                    print_player_view(current_player, players, game_info)
                    view_client_card_play(client_card_play_dict)

                    sockets_to_clients.send_same_message_to_each_client(
                        'client_card_play_dict', client_card_play_dict)

                    client_card_play_dict_is_legal = is_card_play_legal(current_player, players, game_info,
                                                                        client_card_play_dict)
                    # If the play is legal and player does not wish to discard their hand.
                    if client_card_play_dict_is_legal and client_card_play_dict["card"] is not None:
                        # Print that the play is deemed legal
                        print('card play is legal')
                        # resolve client_card_play
                        client_card_play = card_play_dict_to_card_play(client_card_play_dict, current_player, players)
                        do_card_play_and_resolve_outcome(client_card_play, current_player, players, game_info,
                                                         card_plays_on_pawns_and_outcomes=[])
                        # Discard card from hand
                        move_card_from_hand_to_discard_and_mark_in_player_card_history(current_player,
                                                                                       client_card_play["card"],
                                                                                       discard_pile)
                    # If the play is legal and player does wish to discard their hand.
                    elif client_card_play_dict_is_legal and client_card_play_dict["card"] is None:
                        # Discard hand
                        if current_player.hand:
                            discard_pile.extend(current_player.hand[:])
                            current_player.card_history += ''.join(card.rank for card in current_player.hand)
                            current_player.hand[:] = []
                            print('No legal card play available, hand is discarded')
                        else:
                            print('No legal card play available')
                    # If the play is not legal.
                    elif not client_card_play_dict_is_legal:
                        # Play the lowest value card_play
                        all_card_plays = test_all_possible_plays(current_player, players, game_info)
                        legal_card_plays = [card_play for card_play in all_card_plays if
                                            card_play[-1]["card_play_is_legal"]]
                        legal_card_play_board_values = [card_play[0]["board_value"] for card_play in legal_card_plays]
                        worst_card_play_index = legal_card_play_board_values.index(min(legal_card_play_board_values))
                        worst_card_play = legal_card_plays[worst_card_play_index][0]
                        print('Provided card play is illegal. Worst card play was played instead.')
                        print('Substituted card play: ', card_play_to_dict([worst_card_play]))
                        do_card_play_and_resolve_outcome(worst_card_play, current_player, players, game_info,
                                                         card_plays_on_pawns_and_outcomes=[])
                        # Discard card from hand
                        move_card_from_hand_to_discard_and_mark_in_player_card_history(current_player,
                                                                                       worst_card_play["card"],
                                                                                       discard_pile)
                    board_states = create_board_states_per_client(players, deck, game_info)
                    all_pawns_of_current_player_are_in_finish = all([pawn.finish for pawn in current_player.pawns])
                    sockets_to_clients.send_same_message_to_each_client(
                        'all_pawns_of_current_player_are_in_finish', all_pawns_of_current_player_are_in_finish)
                    if all_pawns_of_current_player_are_in_finish:
                        print("player " + str(current_player.color) + ' has won')
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
