from card_play_logic import card_play_to_dict
from card_play_logic import create_card_play
from card import Card
import random
import socket


def get_server_ip():
    server_ip = input("What is the server IP?")
    if server_ip == '0':
        server_ip = socket.gethostbyname(socket.gethostname())
    return server_ip


def player_choice(q1, m1, m2, m3):
    choice = ""
    stupid_player_loop = 0
    while type(choice) is not bool:
        choice = input(q1).casefold()
        if choice == "y":
            choice = True
            print(m1)
        elif choice == "n":
            choice = False
            print(m2)
        else:
            if stupid_player_loop == 0:
                print("Input should be \"Y\" or \"N\". You can do it!")
            elif stupid_player_loop == 1:
                print("It's just one letter. Is that so hard?")
            elif stupid_player_loop == 2:
                print("Come on...")
            elif stupid_player_loop == 3:
                print("I'm warning you...")
            elif stupid_player_loop == 4:
                choice = False
                print(m3)
            stupid_player_loop += 1
    return choice


def is_player_human():
    q1 = "Are you human, Y/N?"
    m1 = "Player is human controlled"
    m2 = "Player is controlled by bot"
    m3 = "Stupid player is controlled by bot. Believe me, it's for the best."
    player_is_human = player_choice(q1, m1, m2, m3)
    return player_is_human


def does_player_want_to_play():
    q1 = "Do you want to play a card, Y/N? \nAnswer \"N\" if you see no legal play:"
    m1 = "Pick a play"
    m2 = "Server will verify if there is nothing to play"
    m3 = "Stupid player has forfeited their choice. Your loss."
    player_wants_to_play = player_choice(q1, m1, m2, m3)
    return player_wants_to_play


def print_player_view(player, players, game_info):
    # Determine player order from clients view
    client_index = game_info.player_colors.index(player.color)
    player_colors_in_turn_order = game_info.player_colors[client_index:] + game_info.player_colors[:client_index]
    all_pawns_on_board = [pawn for pawn in players.all_pawns if not pawn.home and not pawn.finish]
    positions_of_all_pawns_on_board = [pawn.position for pawn in all_pawns_on_board]

    print(f"\n==========================={player.color.upper()}'s turn===========================")
    print("\nSTART\t\t|BOARD")
    for player_color in player_colors_in_turn_order:
        player_turn_index = player_colors_in_turn_order.index(player_color)
        print(f"{player_color.upper()[:8]: <8}\t", end="|")
        for position_from_player_color_start in range(16):
            position = position_from_player_color_start + 16*player_turn_index
            if position in positions_of_all_pawns_on_board:
                pawn_index = positions_of_all_pawns_on_board.index(position)
                # Color strings are limited to 6 characters such that
                # "|" + color_string + "\t" does not exceed two tab lengths (8characters)
                # Similarly, "<6" pads color strings with spaces up to 6 chars, such that
                # "|" + color_string + "\t" is never smaller than two tab lengths (8characters)
                print(f"{all_pawns_on_board[pawn_index].color.casefold()[:6]: <6}\t", end="|")
            elif position % 1 == 0:
                print(f"{str(position)[:6]: <6}\t", end="|")
            else:
                print("\t", end="|")
        print("") # this adds an enter after every line

    # Now for pawns in finish
    print("\nFINISH")
    for player_color in player_colors_in_turn_order:
        all_pawns_in_finish_of_this_color = [pawn for pawn in players.all_pawns if pawn.finish and pawn.color == player_color]
        player_turn_index = player_colors_in_turn_order.index(player_color)
        print(f"{player_color.upper()[:8]: <8}\t", end="|")
        for finish_position in range(4):
            if (finish_position in
                    [pawn.position_from_own_start % game_info.board_size_per_player
                     for pawn in all_pawns_in_finish_of_this_color]):
                print(f"{player_color.casefold()[:6]: <6}\t", end="|")
            elif player_color == player.color:
                finish_position_from_own_start = str(finish_position + game_info.board_size)
                print(f"{finish_position_from_own_start.casefold()[:6]: <6}\t", end="|")
            else:
                print("\t", end="|")
        print("")  # this adds an enter after every line
    print('\n' + player.color + ' hand: ' + ''.join(card.rank for card in player.hand))


def pick_a_pawn(player, players, game_info, my_pawn):
    my_pawns_on_board = [pawn for pawn in player.pawns if not pawn.home]
    other_pawns_on_board = [pawn for pawn in players.other_pawns(player) if not pawn.finish and not pawn.home]
    all_pawns_on_board = my_pawns_on_board + other_pawns_on_board
    positions_of_all_pawns_on_board = [pawn.position for pawn in all_pawns_on_board]
    pawn_is_picked = False
    while not pawn_is_picked:
        pawn_choice = input(f"Pick a pawn by position (0-{game_info.board_size + 3}), at home (H), none (N) "
                            f"or a different card (-1):")
        try:
            pawn_choice = int(pawn_choice)
        except ValueError:
            if pawn_choice.casefold() == 'h':
                try:
                    my_pawn = [pawn for pawn in player.pawns if pawn.home][0]
                    pawn_is_picked = True
                except IndexError:
                    print("There are no pawns in your home base")
            elif pawn_choice.casefold() == 'n':
                my_pawn = None
                pawn_is_picked = True
            else:
                print("Type an int, 'H', or 'N please")
        else:
            if pawn_choice in positions_of_all_pawns_on_board:
                my_pawn_index = positions_of_all_pawns_on_board.index(pawn_choice)
                my_pawn = all_pawns_on_board[my_pawn_index]
                pawn_is_picked = True
            elif pawn_choice == -1:
                retort = random.randint(1, 2)
                if retort == 1:
                    print("Tafel plakt!")
                elif retort == 2:
                    print("No take backsies!")
            else:
                print(f"There is no pawn at {pawn_choice}")
    return my_pawn


def pick_card_play(player, players, game_info):
    if not player.hand:
        card_play_dict = None
        print("Hand is empty, turn is automatically skipped.")
        return card_play_dict

    # Initialize card play variables
    card = ""
    my_pawn = ""
    target_pawn = ""
    move_value = ""

    while type(card) is not Card:
        card_choice = input("Pick a card (A23456789XJQK), or '0' if you can't play:").casefold()
        if card_choice in ''.join(card.rank.casefold() for card in player.hand) and len(card_choice) == 1:
            for a_card in player.hand:
                if a_card.rank.casefold() == card_choice:
                    card = a_card
                    print(f"You have picked {card.rank}")
                    break
        elif card_choice == '0':
            card_play_dict = None
            return card_play_dict
        else:
            card = None
            print(f"\"{card_choice}\" is not in " + ''.join(card.rank for card in player.hand))

    my_pawn = pick_a_pawn(player, players, game_info, my_pawn)
    if card.rank == "J" or card.is_splittable:
        target_pawn = pick_a_pawn(player, players, game_info, target_pawn)
    else:
        target_pawn = None
    if card.is_splittable and target_pawn:
        while type(move_value) is not int:
            move_value = input("How far will your first pawn move?")
            try:
                move_value = int(move_value)
            except ValueError:
                print(f"{move_value} is not an integer")
    else:
        move_value = card.move_value
    card_play = create_card_play(card, my_pawn, target_pawn, move_value, card_play_is_legal=True, board_value=0)
    card_play_dict = card_play_to_dict([card_play])
    return card_play_dict

    # NExt: change this into a GUI, most likely as an object