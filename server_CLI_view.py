
def how_many_players_in_game() -> int:
    while True:
        try:
            player_number = input("How many players are joining? Please state a number <=8: ")  # limit by create_starting_game_ob
            return int(player_number)
        except ValueError as error:
            # log(error)
            print(f'You input {player_number}. Try again.')


def view_client_card_play(client_card_play_dict):
    # log(client_card_play_dict)
    print('client card play: ', client_card_play_dict)
