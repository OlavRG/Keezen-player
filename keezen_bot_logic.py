# -*- coding: utf-8 -*-
"""
Contains all logic that is specific to the Keezen bot. It does not contain logic that is also used by the server or
client.

Created on Wed Feb 05 2025

@author: olavg
"""

from card import Card
import copy
from card_play_logic import test_all_possible_plays
from card_play_logic import do_card_play_and_resolve_outcome
from card_play_logic import move_card_from_hand_to_discard_and_mark_in_player_card_history
from card_play_logic import reset_pawns_to_previous_state
from card_play_logic import create_card_play


def test_next_round_card_plays(player, players, game_info, card_play):
    next_round_hand = []
    all_unique_cards = 'A23456789XJQK'
    for card in all_unique_cards:
        next_round_hand.append(Card(card))
    backup_hand = player.hand[:]
    player.hand = next_round_hand
    next_round_plays = test_all_possible_plays(player, players, game_info)
    player.hand = backup_hand[:]
    card_plays_up_to_next_round = []
    for next_round_play in next_round_plays:
        old_and_new_play = card_play + next_round_play
        card_plays_up_to_next_round.append(old_and_new_play)
    return card_plays_up_to_next_round


def test_all_possible_follow_up_plays(legal_card_plays, dead_end_plays, player, players, game_info, discard_pile):
    """
    Takes a list of legal card play sequences. Each sequence is a list of card plays the player could play this round,
    ordered by index. For each sequence this functions simulates playing it, and then testing any follow-up card play.
    Sequences that result in discarding part of the hand are stored in dead_end_plays (and are legal!), the rest in
    legal_card_plays.
    :param legal_card_plays:
    :param dead_end_plays:
    :param player:
    :param players:
    :param game_info:
    :param discard_pile:
    :return:
    """
    all_card_plays = []
    backup_player_card_history = player.card_history
    my_backup_pawns = copy.deepcopy(player.pawns)
    other_backup_pawns = copy.deepcopy(players.other_pawns(player))
    backup_hand = player.hand[:]
    backup_discard_pile = discard_pile[:]
    for consecutive_card_plays in legal_card_plays:
        for card_play in consecutive_card_plays:
            do_card_play_and_resolve_outcome(card_play, player, players, game_info,
                                             card_plays_on_pawns_and_outcomes=[])
            # Discard card from hand
            move_card_from_hand_to_discard_and_mark_in_player_card_history(player, card_play["card"], discard_pile)
        new_card_plays_from_single_previous_play = test_all_possible_plays(player, players, game_info)
        # if previous turn play has no follow up, check the value of its next round
        legal_new_card_plays_from_single_previous_play = [new_card_play for new_card_play in
                                                          new_card_plays_from_single_previous_play if
                                                          new_card_play[0]["card_play_is_legal"]]
        if not legal_new_card_plays_from_single_previous_play:
            dead_end_plays_incl_illegal = test_next_round_card_plays(player, players, game_info, consecutive_card_plays)
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
        reset_pawns_to_previous_state(other_backup_pawns, players.other_pawns(player))
        discard_pile = backup_discard_pile[:]

        # Append the previous play and new play in the same sublist
        for new_turn_card_play in new_card_plays_from_single_previous_play:
            old_and_new_play_from_single_previous_play = consecutive_card_plays + new_turn_card_play
            all_card_plays.append(old_and_new_play_from_single_previous_play)

    # filter all illegal plays
    all_legal_card_plays = [card_play for card_play in all_card_plays if card_play[-1]["card_play_is_legal"]]

    return all_legal_card_plays, dead_end_plays


def pick_play_with_highest_eventual_board_value(all_plays) -> dict:
    """
    Takes the output of test_all_possible_follow_up_plays (or an empty card play) and finds the one that ends with the
    greatest board_value.
    :param all_plays:  A list of lists. Every sub-list is a sequence of card plays a player could legally make this round.
    :return: a card play dict, formatted as card_play
    """
    highest_value = -1  # -1 to be lower than 0, the value of an empty card_play
    best_play = None  # There should always be a card play as input, so this should always be overwritten
    for play in all_plays:
        if play[-1]["board_value"] > highest_value:
            highest_value = play[-1]["board_value"]
            best_play = play[0]
        else:
            pass
    return best_play
