from network import ClientNetwork
from keezen_bot import keezen_bot
import client_view


def main(server_ip):
    socket_to_server = ClientNetwork(server_ip)
    all_pawns_of_current_player_are_in_finish = False
    player_is_human = client_view.is_player_human()
    socket_to_server.connect()
    while not all_pawns_of_current_player_are_in_finish:
        message = socket_to_server.receive()
        match message["header"]:
            case 'view_board_state':
                board_state = message["content"]
                # Parse board state, return pawn objects, hand object, player object
                [player, current_player_color, other_pawns, discard_pile, game_info] = client_view.create_game_objects_from_board_state(board_state)

                client_view.print_player_view(player, current_player_color, other_pawns, game_info)

            case 'play_from_board_state':
                board_state = message["content"]
                # Parse board state, return pawn objects, hand object, player object
                [player, current_player_color, other_pawns, discard_pile, game_info] = client_view.create_game_objects_from_board_state(board_state)
                if not player_is_human:
                    card_play = keezen_bot(board_state)
                else:
                    card_play = client_view.pick_card_play(player, other_pawns, game_info)
                socket_to_server.send(card_play)

            case 'client_card_play_dict':
                client_card_play_dict = message["content"]
                if not client_card_play_dict:
                    print('Player does not want to play a card')
                elif not client_card_play_dict['secondary_pawn_color']:
                    print(f'Player wants to play {client_card_play_dict["card"]} '
                          f'on {client_card_play_dict["primary_pawn_color"]} '
                          f'at {client_card_play_dict["primary_pawn_position"]}')
                elif client_card_play_dict['secondary_pawn_color'] and client_card_play_dict['primary_move']:
                    print(f'Player wants to play {client_card_play_dict["card"]} '
                          f'on {client_card_play_dict["primary_pawn_color"]} '
                          f'at {client_card_play_dict["primary_pawn_position"]} '
                          f'for {client_card_play_dict["primary_move"]} steps, '
                          f'and on {client_card_play_dict["secondary_pawn_color"]} '
                          f'at {client_card_play_dict["secondary_pawn_position"]} for the remainder')
                elif client_card_play_dict['secondary_pawn_color'] and not client_card_play_dict['primary_move']:
                    print(f'Player wants to play {client_card_play_dict["card"]} '
                          f'on {client_card_play_dict["primary_pawn_color"]} '
                          f'at {client_card_play_dict["primary_pawn_position"]} '
                          f'and on {client_card_play_dict["secondary_pawn_color"]} '
                          f'at {client_card_play_dict["secondary_pawn_position"]}')
                else:
                    print('Unexpected card play received')
            case 'all_pawns_of_current_player_are_in_finish':
                all_pawns_of_current_player_are_in_finish = message["content"]
                print('Did the current player win? ' + str(all_pawns_of_current_player_are_in_finish))


if __name__ == "__main__":
    server_IP = input("What is the server IP?")
    main(server_IP)
