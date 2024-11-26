# FUNCTION
# This script contains all functions for resolving a card_play and the testing of card_plays. A card_play is defined as
# all information describing a players intended action in a turn, and optionally the legality and resulting board_value.

from is_card_play_legal import is_card_play_legal
import copy
from board_value import get_board_value
from card import Card
from pawn import Pawn
from game_info import GameInfo
from player import Player


def check_for_tackled_pawn_and_move_them_home(my_pawn, my_pawns, other_pawns):
    my_other_pawns = [value for value in my_pawns if value != my_pawn]
    for target_pawn in my_other_pawns + other_pawns:
        if my_pawn.position == target_pawn.position:
            target_pawn.move_home()


def create_card_play(card, my_pawn, target_pawn=None, move_value=None, card_play_is_legal=False, board_value=0):
    return {"card": card, "primary_pawn": my_pawn,
            "secondary_pawn": target_pawn, "primary_move": move_value,
            "card_play_is_legal": card_play_is_legal,
            "board_value": board_value}


def do_card_play_and_resolve_outcome(card_play, player, other_pawns,
                                     game_info, card_plays_on_pawns_and_outcomes) -> object:
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
    card_play_is_legal_p1 = is_card_play_legal(card_play["primary_pawn"], my_other_pawns, other_pawns,
                                               move_value, game_info)

    # check legality for target pawn
    if card_play["secondary_pawn"]:
        other_pawns_owned_by_target = [pawn for pawn in [card_play["primary_pawn"]] + my_other_pawns + other_pawns if
                                       pawn.color == card_play["secondary_pawn"].color and pawn != card_play["secondary_pawn"]]
        pawns_not_owned_by_target = [pawn for pawn in [card_play["primary_pawn"]] + my_other_pawns + other_pawns if
                                     pawn.color != card_play["secondary_pawn"].color]
        card_play_is_legal_p2 = is_card_play_legal(card_play["secondary_pawn"], other_pawns_owned_by_target, pawns_not_owned_by_target,
                                                   move_2, game_info)
    else:
        card_play_is_legal_p2 = True

    card_play_is_legal = card_play_is_legal_p1 & card_play_is_legal_p2

    # If a pawn was tackled during move, move it off the board here. This must be done after card_play_is_legal, since
    # that function checks for protected pawns being illegally tackled
    check_for_tackled_pawn_and_move_them_home(card_play["primary_pawn"], [card_play["primary_pawn"]] + my_other_pawns, other_pawns)
    if card_play["secondary_pawn"]:
        other_pawns_owned_by_target = [pawn for pawn in [card_play["primary_pawn"]] + my_other_pawns + other_pawns if
                                       pawn.color == card_play["secondary_pawn"].color and pawn != card_play["secondary_pawn"]]
        pawns_not_owned_by_target = [pawn for pawn in [card_play["primary_pawn"]] + my_other_pawns + other_pawns if
                                     pawn.color != card_play["secondary_pawn"].color]
        check_for_tackled_pawn_and_move_them_home(card_play["secondary_pawn"], other_pawns_owned_by_target, pawns_not_owned_by_target)

    for pawn in [card_play["primary_pawn"]] + my_other_pawns + other_pawns:
        pawn.reset_start_of_turn_bools_for_next_turn()

    # get board value
    board_value = get_board_value([card_play["primary_pawn"]] + my_other_pawns, other_pawns, game_info)
    card_plays_on_pawns_and_outcomes.append([create_card_play(card_play["card"], card_play["primary_pawn"], card_play["secondary_pawn"],
                                                              move_value, card_play_is_legal, board_value)])

    return card_plays_on_pawns_and_outcomes, [card_play["primary_pawn"]] + my_other_pawns, other_pawns


def reset_pawns_to_previous_state(backup_pawns, pawns):
    for pawn_number in range(len(pawns)):
        pawns[pawn_number].__dict__.update(backup_pawns[pawn_number].__dict__)


# test the outcome of a play without playing it (like playing it in your mind)
def test_all_possible_plays(player, other_pawns, discard_pile, game_info):
    my_backup_pawns = copy.deepcopy(player.pawns)
    other_backup_pawns = copy.deepcopy(other_pawns)
    card_plays_on_pawns_and_outcomes = []
    for card in player.hand:
        for my_pawn in player.pawns:
            card_play = create_card_play(card, my_pawn)
            my_other_pawns = [value for value in player.pawns if value != my_pawn]
            if card.is_splittable:
                do_card_play_and_resolve_outcome(card_play, player, other_pawns, game_info,
                                                 card_plays_on_pawns_and_outcomes)
                # reset pawns back to original position
                reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
                reset_pawns_to_previous_state(other_backup_pawns, other_pawns)
                for my_other_pawn in my_other_pawns:
                    for move_1 in range(1, card.move_value):
                        card_play["secondary_pawn"] = my_other_pawn
                        card_play["primary_move"] = move_1
                        do_card_play_and_resolve_outcome(card_play, player, other_pawns, game_info,
                                                         card_plays_on_pawns_and_outcomes)
                        # reset pawns back to original position
                        reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
                        reset_pawns_to_previous_state(other_backup_pawns, other_pawns)

            elif card.rank == 'J':
                for other_pawn in other_pawns:
                    card_play["secondary_pawn"] = other_pawn
                    do_card_play_and_resolve_outcome(card_play, player, other_pawns, game_info,
                                                     card_plays_on_pawns_and_outcomes)
                    # reset pawns back to original position
                    reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
                    reset_pawns_to_previous_state(other_backup_pawns, other_pawns)

            else:
                do_card_play_and_resolve_outcome(card_play, player, other_pawns, game_info,
                                                 card_plays_on_pawns_and_outcomes)
                # reset pawns back to original position
                reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
                reset_pawns_to_previous_state(other_backup_pawns, other_pawns)
    return card_plays_on_pawns_and_outcomes


def test_next_round_card_plays(player, other_pawns, discard_pile, game_info, card_play):
    next_round_hand = []
    all_unique_cards = 'A23456789XJQK'
    for card in all_unique_cards:
        next_round_hand.append(Card(card))
    backup_hand = player.hand[:]
    player.hand = next_round_hand
    next_round_plays = test_all_possible_plays(player, other_pawns, discard_pile, game_info)
    player.hand = backup_hand[:]
    card_plays_up_to_next_round = []
    for next_round_play in next_round_plays:
        old_and_new_play = card_play + next_round_play
        card_plays_up_to_next_round.append(old_and_new_play)
    return card_plays_up_to_next_round


def test_all_possible_follow_up_plays(legal_card_plays, dead_end_plays, player, other_pawns, game_info, discard_pile):
    all_card_plays = []
    backup_player_card_history = player.card_history
    my_backup_pawns = copy.deepcopy(player.pawns)
    other_backup_pawns = copy.deepcopy(other_pawns)
    backup_hand = player.hand[:]
    backup_discard_pile = discard_pile[:]
    for consecutive_card_plays in legal_card_plays:
        for card_play in consecutive_card_plays:
            do_card_play_and_resolve_outcome(card_play, player, other_pawns, game_info,
                                             card_plays_on_pawns_and_outcomes=[])
            # Discard card from hand
            move_card_from_hand_to_discard_and_mark_in_player_card_history(player, card_play["card"], discard_pile)
        new_card_plays_from_single_previous_play = test_all_possible_plays(player, other_pawns, discard_pile, game_info)
        # if previous turn play has no follow up, check the value of its next round
        legal_new_card_plays_from_single_previous_play = [new_card_play for new_card_play in
                                                          new_card_plays_from_single_previous_play if
                                                          new_card_play[0]["card_play_is_legal"]]
        if not legal_new_card_plays_from_single_previous_play:
            dead_end_plays_incl_illegal = test_next_round_card_plays(player, player.pawns, other_pawns, game_info, consecutive_card_plays)
            dead_end_plays += [play for play in dead_end_plays_incl_illegal if play[-1]["card_play_is_legal"]]
            # Putting the last pawn in finish leaves no legal new card plays. Hence we check separately for a winning move
            if all([pawn.finish for pawn in player.pawns]):
                dead_end_plays += [consecutive_card_plays]
        else:
            pass

        # reset test pawns and hand for following loop
        player.card_history = backup_player_card_history
        reset_pawns_to_previous_state(my_backup_pawns, player.pawns)
        player.hand = backup_hand[:]
        reset_pawns_to_previous_state(other_backup_pawns, other_pawns)
        discard_pile = backup_discard_pile[:]

        # Append the previous play and new play in the same sublist
        for new_turn_card_play in new_card_plays_from_single_previous_play:
            old_and_new_play_from_single_previous_play = consecutive_card_plays + new_turn_card_play
            all_card_plays.append(old_and_new_play_from_single_previous_play)

    # filter all illegal plays
    all_legal_card_plays = [card_play for card_play in all_card_plays if card_play[-1]["card_play_is_legal"]]

    return all_legal_card_plays, dead_end_plays


def pick_play_with_highest_eventual_board_value(all_plays):
    highest_value = 0
    best_play = None
    for play in all_plays:
        if play[-1]["board_value"] > highest_value:
            highest_value = play[-1]["board_value"]
            best_play = play
        else:
            pass
    return best_play


def card_play_to_dict(card_play):
    # check if there is any legal play
    if not card_play:
        card_play_dict = None
        return card_play_dict
    else:
        card_play = card_play[0]
    if card_play["secondary_pawn"]:
        secondary_pawn_color = card_play["secondary_pawn"].color
        secondary_pawn_position = card_play["secondary_pawn"].position_from_own_start
    else:
        secondary_pawn_color = None
        secondary_pawn_position = None
    # primary_pawn_home is needed to distinguish between pawns at position 0 on the board and at home
    card_play_dict = {"card": card_play["card"].rank,
                      "primary_pawn_color": card_play["primary_pawn"].color,
                      "primary_pawn_position": card_play["primary_pawn"].position_from_own_start,
                      "primary_pawn_home": card_play["primary_pawn"].home,
                      "secondary_pawn_color": secondary_pawn_color,
                      "secondary_pawn_position": secondary_pawn_position,
                      "primary_move": card_play["primary_move"]}
    return card_play_dict


def move_card_from_hand_to_discard_and_mark_in_player_card_history(player: Player, card: Card, discard_pile: list):
    player.card_history += card.rank
    card_index_in_hand = player.hand.index(card)
    discard_pile.append(player.hand.pop(card_index_in_hand))
    return player, discard_pile
