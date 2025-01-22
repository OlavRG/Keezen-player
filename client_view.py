from card_play_logic import card_play_to_dict
from card_play_logic import create_card_play
from board_state_logic import create_game_objects_from_board_state
from card import Card
from pawn import Pawn
from game_info import GameInfo
import random
import socket
#from rich import print


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


def print_player_view(player, current_player_color, other_pawns, game_info):
    # Determine player order from clients view
    client_index = game_info.player_colors.index(player.color)
    player_colors_in_turn_order = game_info.player_colors[client_index:] + game_info.player_colors[:client_index]
    all_pawns = player.pawns + other_pawns
    all_pawns_on_board = [pawn for pawn in all_pawns if not pawn.home and not pawn.finish]
    positions_of_all_pawns_on_board = [pawn.position for pawn in all_pawns_on_board]

    print(f"\n==========================={current_player_color.upper()}'s turn===========================")
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
        all_pawns_in_finish_of_this_color = [pawn for pawn in all_pawns if pawn.finish and pawn.color == player_color]
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


def pick_a_pawn(player, other_pawns, game_info, my_pawn):
    my_pawns_on_board = [pawn for pawn in player.pawns if not pawn.home]
    other_pawns_on_board = [pawn for pawn in other_pawns if not pawn.finish and not pawn.home]
    all_pawns_on_board = my_pawns_on_board + other_pawns_on_board
    positions_of_all_pawns_on_board = [pawn.position for pawn in all_pawns_on_board]
    while type(my_pawn) is not Pawn:
        pawn_choice = input(f"Pick a pawn by position (0-{game_info.board_size + 3}), at home (H), "
                            f"or a different card (-1):")
        try:
            pawn_choice = int(pawn_choice)
        except ValueError:
            if pawn_choice.casefold() == 'h':
                try:
                    my_pawn = [pawn for pawn in player.pawns if pawn.home][0]
                except IndexError:
                    print("There are no pawns in your home base")
            else:
                print("Type an int or 'H' please")
        else:
            if pawn_choice in positions_of_all_pawns_on_board:
                my_pawn_index = positions_of_all_pawns_on_board.index(pawn_choice)
                my_pawn = all_pawns_on_board[my_pawn_index]
            elif pawn_choice == -1:
                retort = random.randint(1, 2)
                if retort == 1:
                    print("Tafel plakt!")
                elif retort == 2:
                    print("No take backsies!")
            else:
                print(f"There is no pawn at {pawn_choice}")
    return my_pawn


def pick_card_play(player, other_pawns, game_info):
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

    my_pawn = pick_a_pawn(player, other_pawns, game_info, my_pawn)
    """
    my_pawns_on_board = [pawn for pawn in player.pawns if not pawn.home]
    other_pawns_on_board = [pawn for pawn in other_pawns if not pawn.finish and not pawn.home]
    all_pawns_on_board = my_pawns_on_board + other_pawns_on_board
    positions_of_all_pawns_on_board = [pawn.position for pawn in all_pawns_on_board]
    while type(my_pawn) is not Pawn:
        pawn_choice = input(f"Pick a pawn by position (0-{game_info.board_size + 3}), at home (H), "
                            f"or a different card (-1):")
        try:
            pawn_choice = int(pawn_choice)
        except ValueError:
            if pawn_choice.casefold() == 'h':
                try:
                    my_pawn = [pawn for pawn in player.pawns if pawn.home][0]
                except IndexError:
                    print("There are no pawns in your home base")
            else:
                print("Type an int or 'H' please")
        else:
            if pawn_choice in positions_of_all_pawns_on_board:
                my_pawn_index = positions_of_all_pawns_on_board.index(pawn_choice)
                my_pawn = all_pawns_on_board[my_pawn_index]
            elif pawn_choice == -1:
                retort = random.randint(1, 2)
                if retort == 1:
                    print("Tafel plakt!")
                elif retort == 2:
                    print("No take backsies!")
            else:
                print(f"There is no pawn at {pawn_choice}")
    """

    if card.is_splittable or card.rank == "J":
        target_pawn = pick_a_pawn(player, other_pawns, game_info, target_pawn)
        """
        while type(target_pawn) is not Pawn:
            target_pawn_choice = input("Pick a second pawn by #, or '0' for no second pawn:")
            try:
                target_pawn_choice = int(target_pawn_choice)
            except ValueError:
                print(f"{target_pawn_choice} is not int.")
            else:
                if target_pawn_choice in range(1, len(player.pawns + other_pawns) + 1):
                    # Note that the pawn order here must match the pawn order in print_player_view
                    target_pawn = ([pawn for pawn in player.pawns + other_pawns if
                                    not pawn.home and pawn.color == player.color or
                                    not pawn.home and pawn.color != player.color and not pawn.finish] +
                                   [pawn for pawn in player.pawns + other_pawns if pawn.home] +
                                   [pawn for pawn in player.pawns + other_pawns if
                                    pawn.color != player.color and pawn.finish])[target_pawn_choice - 1]
                elif target_pawn_choice == 0:
                    target_pawn = None
                    break
                else:
                    print(f"Pick a pawn between 1 and {len(player.pawns + other_pawns)}")
        """
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