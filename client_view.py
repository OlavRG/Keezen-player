from card_play_logic import card_play_to_dict
from card_play_logic import create_card_play
from board_state_logic import create_game_objects_from_board_state
from card import Card
from pawn import Pawn
from game_info import GameInfo


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


def print_player_view(player, other_pawns):
    print(f"\n--------------------------{player.color.upper()}--------------------------")
    print("Pawns on the board:")
    pawn_counter = 1
    for pawn in player.pawns + other_pawns:
        if (not pawn.home and pawn.color == player.color or
                not pawn.home and pawn.color != player.color and not pawn.finish):
            print(f"{pawn_counter}. " + str(pawn))
            pawn_counter += 1
    print("\nPawns off the board:")
    for pawn in player.pawns + other_pawns:
        if pawn.home:
            print(f"{pawn_counter}. " + str(pawn))
            pawn_counter += 1
    print("\nEnemy pawns in finish:")
    for pawn in player.pawns + other_pawns:
        if pawn.color != player.color and pawn.finish:
            print(f"{pawn_counter}. " + str(pawn))
            pawn_counter += 1
    print(player.color + ' hand: ' + ''.join(card.rank for card in player.hand))

def print_board_overview(player, other_pawns, game_info, ):
    print(f"\n--------------------------{player.color.upper()}--------------------------")
    for player_color in game_info.player_colors:
        print(f"\n{player_color.upper()[:6]} START\t| 1\t| 2\t| 3\t| 4\t| 5\t| 6\t| 7\t| 8\t| 9\t| 10\t| 11\t| 12\t| 13\t"
              f"| 14\t| 15\t|")
        print(f"\t\t| 1\t| 2\t| 3\t| 4\t| 5\t| 6\t| 7\t| 8\t| 9\t| 10\t| 11\t| 12\t| 13\t"
              f"| 14\t| 15\t|")

    for board_space in game_info.board_size:
        print(f"\n\t{board_space} | loc\t\t| pawn")


def pick_card_play(board_state):
    # Parse board state, return pawn objects, hand object, player object
    [player, other_pawns, discard_pile, game_info] = create_game_objects_from_board_state(board_state)

    print_player_view(player, other_pawns)

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

    while type(my_pawn) is not Pawn:
        pawn_choice = input("Pick a pawn by #:")
        try:
            pawn_choice = int(pawn_choice)
        except ValueError:
            print("Type an int please")
        else:
            if pawn_choice in range(1, len(player.pawns + other_pawns)+1):
                # Note that the pawn order here must match the pawn order in print_player_view
                my_pawn = ([pawn for pawn in player.pawns + other_pawns if
                            not pawn.home and pawn.color == player.color or
                            not pawn.home and pawn.color != player.color and not pawn.finish] +
                           [pawn for pawn in player.pawns + other_pawns if pawn.home] +
                           [pawn for pawn in player.pawns + other_pawns if
                            pawn.color != player.color and pawn.finish])[pawn_choice-1]
            else:
                print(f"Pick a pawn between 1 and {len(player.pawns + other_pawns)}")
    if card.is_splittable or card.rank == "J":
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


"""
# Following is code for an interface that allows illegal plays to be passed.
        card_choice = input("Pick a card from your hand by typing the appropriate letter. Legal values are "
                            "A23456789XJQK.")
        if card_choice == "K":
            home_choice = True
        elif card_choice is not "A" and card_choice is not "K":
            home_choice = False
        else:
            home_choice = input("You want to play \"A\". Do you want to place a new pawn on the board, Y/N?")
            if home_choice == "Y":
                home_choice = True
            else:
                home_choice = False
        pawn_choice = input(
            "Now type the position (int) of the target pawn")

        card_play_dict = {"card": card_choice,
                          "primary_pawn_color": player.color,
                          "primary_pawn_position": pawn_choice,
                          "primary_pawn_home": home_choice,
                          "secondary_pawn_color": secondary_pawn_color,
                          "secondary_pawn_position": secondary_pawn_position,
                          "primary_move": card_play["primary_move"]}

"""