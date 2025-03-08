# FUNCTION
# This script contains all functions for creating and resolving card_plays. It also contains the testing of all
# card_plays in a single turn. A card_play is defined as all information describing a players intended action in a turn,
# and optionally the legality and resulting board_value. Functions looking at card_plays of consecutive turns are
# captured in keezen_bot_logic.py.

from is_pawn_move_legal import is_pawn_move_legal
import copy
from board_value import get_board_value
from card import Card
from pawn import Pawn
from game_info import GameInfo
from player import Player


def check_for_tackled_pawn_and_move_them_home(my_pawn, players):
    for target_pawn in [pawn for pawn in players.all_pawns if pawn != my_pawn]:
        if my_pawn.position == target_pawn.position and not target_pawn.finish: # finish should be implemented better
            target_pawn.move_home()


def create_card_play(card, my_pawn, target_pawn=None, move_value=None, card_play_is_legal=False, board_value=0):
    return {"card": card, "primary_pawn": my_pawn,
            "secondary_pawn": target_pawn, "primary_move": move_value,
            "card_play_is_legal": card_play_is_legal,
            "board_value": board_value}


def do_card_play_and_resolve_outcome(card_play, player, players,
                                     game_info, card_plays_on_pawns_and_outcomes):
    my_other_pawns = [pawn for pawn in player.pawns if pawn != card_play["primary_pawn"]]
    position_1 = card_play["primary_pawn"].position
    if card_play["primary_move"]:
        move_value = card_play["primary_move"]
        move_2 = card_play["card"].move_value - card_play["primary_move"]
    else:
        move_value = card_play["card"].move_value
        move_2 = 0

    if card_play["secondary_pawn"]:
        position_2 = card_play["secondary_pawn"].position
    else:
        position_2 = None

    # move pawns according to move values
    card_play["primary_pawn"].move_by_card(card_play["card"], game_info, move_from_7=card_play["primary_move"], jack_other_pawn_position=position_2)
    if card_play["secondary_pawn"]:
        card_play["secondary_pawn"].move_by_card(card_play["card"], game_info, move_from_7=move_2, jack_other_pawn_position=position_1)
    else:
        pass

    # check if move is legal
    card_play_is_legal_p1 = is_pawn_move_legal(card_play["primary_pawn"], my_other_pawns, players.other_pawns(player),
                                               move_value, game_info)

    # check legality for target pawn
    if card_play["secondary_pawn"]:
        other_pawns_owned_by_target = [pawn for pawn in players.all_pawns if
                                       pawn.color == card_play["secondary_pawn"].color and pawn != card_play["secondary_pawn"]]
        pawns_not_owned_by_target = [pawn for pawn in players.all_pawns if
                                     pawn.color != card_play["secondary_pawn"].color]
        card_play_is_legal_p2 = is_pawn_move_legal(card_play["secondary_pawn"], other_pawns_owned_by_target, pawns_not_owned_by_target,
                                                   move_2, game_info)
    else:
        card_play_is_legal_p2 = True

    card_play_is_legal = card_play_is_legal_p1 & card_play_is_legal_p2

    # If a pawn was tackled during move, move it off the board here. This must be done after card_play_is_legal, since
    # that function checks for protected pawns being illegally tackled
    check_for_tackled_pawn_and_move_them_home(card_play["primary_pawn"], players)
    if card_play["secondary_pawn"]:
        check_for_tackled_pawn_and_move_them_home(card_play["secondary_pawn"], players)

    for pawn in players.all_pawns:
        pawn.reset_start_of_turn_bools_for_next_turn()

    # get board value
    board_value = get_board_value(player.pawns, game_info)
    card_plays_on_pawns_and_outcomes.append([create_card_play(card_play["card"], card_play["primary_pawn"], card_play["secondary_pawn"],
                                                              move_value, card_play_is_legal, board_value)])

    return card_plays_on_pawns_and_outcomes, [card_play["primary_pawn"]] + my_other_pawns, players.other_pawns(player)


def reset_pawns_to_previous_state(backup_pawns, pawns):
    for number, pawn in enumerate(pawns):
        pawns[number].__dict__.update(backup_pawns[number].__dict__)


def test_all_possible_plays(player, players, game_info):
    """
    Test every card and pawn combination of the player (and other players pawns for 7s and Js).
    :param player:
    :param players:
    :param game_info:
    :return: List of all card plays, formatted as card_play
    """
    my_backup_pawns = copy.deepcopy(player.pawns)
    other_backup_pawns = copy.deepcopy(players.other_pawns(player))
    card_plays_on_pawns_and_outcomes = []
    for card in player.hand:
        for my_pawn in player.pawns:
            card_play = create_card_play(card, my_pawn)
            my_other_pawns = [value for value in player.pawns if value != my_pawn]
            if card.is_splittable:
                do_card_play_and_resolve_outcome(card_play, player, players, game_info,
                                                 card_plays_on_pawns_and_outcomes)
                # reset pawns back to original position
                reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
                reset_pawns_to_previous_state(other_backup_pawns, players.other_pawns(player))
                for my_other_pawn in my_other_pawns:
                    for move_1 in range(1, card.move_value):
                        card_play["secondary_pawn"] = my_other_pawn
                        card_play["primary_move"] = move_1
                        do_card_play_and_resolve_outcome(card_play, player, players, game_info,
                                                         card_plays_on_pawns_and_outcomes)
                        # reset pawns back to original position
                        reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
                        reset_pawns_to_previous_state(other_backup_pawns, players.other_pawns(player))

            elif card.rank == 'J':
                for other_pawn in players.other_pawns(player):
                    card_play["secondary_pawn"] = other_pawn
                    do_card_play_and_resolve_outcome(card_play, player, players, game_info,
                                                     card_plays_on_pawns_and_outcomes)
                    # reset pawns back to original position
                    reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
                    reset_pawns_to_previous_state(other_backup_pawns, players.other_pawns(player))

            else:
                do_card_play_and_resolve_outcome(card_play, player, players, game_info,
                                                 card_plays_on_pawns_and_outcomes)
                # reset pawns back to original position
                reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
                reset_pawns_to_previous_state(other_backup_pawns, players.other_pawns(player))
    return card_plays_on_pawns_and_outcomes


def is_card_play_legal(player, players, game_info, client_card_play_dict):
    # Make a list of all possible plays and check if the clients move is in it
    all_card_plays = test_all_possible_plays(player, players, game_info)
    legal_card_plays = [card_play[0] for card_play in all_card_plays if card_play[-1]["card_play_is_legal"]]
    if not legal_card_plays:   # In case no card can be played, an empty card_play is expected as input
        legal_card_plays.append(create_card_play(None,None,))
    legal_card_play_dicts = list(map(card_play_to_dict, legal_card_plays))
    client_card_play_is_legal = False
    if client_card_play_dict in legal_card_play_dicts:
        client_card_play_is_legal = True
        return client_card_play_is_legal
    else:
        return client_card_play_is_legal


def card_play_to_dict(card_play: dict):
    """
    :param card_play: dict that contains game object like Pawn, Card, and some values
    :return: card play dict that only contains strings and ints. Primarily used for communication over network
    """
    # check if there is any legal play
    if not card_play["card"]:
        # A card_play_dict with None means the player does not play a card and instead wants to discard their hand
        card_play_dict = {"card": None,
                          "primary_pawn_color": None,
                          "primary_pawn_position": None,
                          "primary_pawn_home": None,
                          "primary_pawn_finish": None,
                          "secondary_pawn_color": None,
                          "secondary_pawn_position": None,
                          "secondary_pawn_home": None,
                          "secondary_pawn_finish": None,
                          "primary_move": None}
        return card_play_dict
    if card_play["secondary_pawn"]:
        secondary_pawn_color = card_play["secondary_pawn"].color
        secondary_pawn_position_from_own_start = card_play["secondary_pawn"].position_from_own_start
        secondary_pawn_home = card_play["secondary_pawn"].home
        secondary_pawn_finish = card_play["secondary_pawn"].finish
    else:
        secondary_pawn_color = None
        secondary_pawn_position_from_own_start = None
        secondary_pawn_home = None
        secondary_pawn_finish = None
    # primary_pawn_home is needed to distinguish between pawns at position 0 on the board and at home
    card_play_dict = {"card": card_play["card"].rank,
                      "primary_pawn_color": card_play["primary_pawn"].color,
                      "primary_pawn_position": card_play["primary_pawn"].position_from_own_start,
                      "primary_pawn_home": card_play["primary_pawn"].home,
                      "primary_pawn_finish": card_play["primary_pawn"].finish,
                      "secondary_pawn_color": secondary_pawn_color,
                      "secondary_pawn_position": secondary_pawn_position_from_own_start,
                      "secondary_pawn_home": secondary_pawn_home,
                      "secondary_pawn_finish": secondary_pawn_finish,
                      "primary_move": card_play["primary_move"]}
    return card_play_dict


def card_play_dict_to_card_play(card_play_dict, player, players):
    # This functions assumes the card and pawns from the dict exist in the player object. Error handling should be
    # added for cases where card_play_dict describes cards, pawns that do not exist
    eligible_cards = [card for card in player.hand if card.rank == card_play_dict["card"]]
    try:
        card = eligible_cards[0]
    except IndexError as error:
        print(f'Card "{card_play_dict["card"]}" in card play dict does not match any card in players hand.')
        print(f'Player hand: {"".join(card.rank for card in player.hand)}')
        print(error)
    eligible_pawns = [pawn for pawn in player.pawns if pawn.color == card_play_dict["primary_pawn_color"]
                      and pawn.position_from_own_start == card_play_dict["primary_pawn_position"]]
    my_pawn = eligible_pawns[0] # pawns can have identical position when they are home
    eligible_target_pawns = [pawn for pawn in players.all_pawns if pawn.color == card_play_dict["secondary_pawn_color"]
                             and pawn.position_from_own_start == card_play_dict["secondary_pawn_position"]]
    try:
        target_pawn = eligible_target_pawns[0]
    except IndexError as error:
        target_pawn = None
    move_value = card_play_dict["primary_move"]
    return create_card_play(card, my_pawn, target_pawn, move_value, card_play_is_legal=False, board_value=0)


def move_card_from_hand_to_discard_and_mark_in_player_card_history(player: Player, card: Card, discard_pile: list):
    player.card_history += card.rank
    card_index_in_hand = player.hand.index(card)
    discard_pile.append(player.hand.pop(card_index_in_hand))
    return player, discard_pile
