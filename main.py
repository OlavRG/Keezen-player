# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 11:22:10 2022

@author: olavg
"""

from board_state_format import board_state
from parse_board_state import parse_board_state
from card_play_logic import test_all_possible_plays
from card_play_logic import test_all_possible_follow_up_plays
from card_play_logic import pick_play_with_highest_eventual_board_value
from card import Card
from board_state_niche_tester import board_state

if __name__ == '__main__':
    # This is the main executable that imports all classes to run a game

    # import and parse board state, return pawn objects, hand object, player object
    [player, my_pawns, other_pawns, hand, game_info] = parse_board_state(board_state)

    all_non_dead_plays = []
    all_dead_plays = []
    # turn 1
    turn_1_plays = test_all_possible_plays(player, my_pawns, other_pawns, hand, game_info)
    turn_1_legal_plays = [card_play for card_play in turn_1_plays if card_play[-1]["card_play_is_legal"]]
    if not turn_1_legal_plays:
        # Discard hand
        Final_play = None
    else:
        # all other turns
        for turn in range(2, len(hand)+1):
            if turn == 2:
                all_non_dead_plays, all_dead_plays = (
                    test_all_possible_follow_up_plays(player, my_pawns, other_pawns, hand, game_info,
                                                      turn_1_legal_plays, all_dead_plays))
            else:
                all_non_dead_plays, all_dead_plays = (
                    test_all_possible_follow_up_plays(player, my_pawns, other_pawns, hand, game_info,
                                                      all_non_dead_plays, all_dead_plays))

    # First turn of next round. Hand contains all cards to test all
    next_round_hand = []
    all_unique_cards = 'A23456789XJQK'
    for card in all_unique_cards:
        next_round_hand.append(Card(card))
    all_non_dead_plays = test_all_possible_follow_up_plays(player, my_pawns, other_pawns, next_round_hand, game_info,
                                                           all_non_dead_plays, [])[0]

    Final_play = pick_play_with_highest_eventual_board_value(all_non_dead_plays + all_dead_plays)

    def print_plays_properly(plays):
        for play in plays:
            for turn in range(0, len(play)):
                print(play[turn]["card"].rank + ' on ' + str(play[turn]["primary_pawn"].position))
                if turn == len(play)-1: print('end play\n')
                else: pass
        print('len(plays) = ' + str(len(plays)))

    print_plays_properly(all_non_dead_plays)

    # next: for board_state_format all_non_dead_plays and all_dead_plays are OK! For Niche: why is 7 not played in all_dead_plays?

    bla = 1


"""
                if not move_is_legal(bla):
                    board_value = 0
                board_value = get_board_value()
                if board_value > highest_board_value:
                    highest_board_value = board_value
"""

# For every card in hand, test-play the card on every pawn and find the new position
# test if this is a legal move
# calculate the board value
# add the board value to the board_value overview
