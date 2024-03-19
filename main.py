# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 11:22:10 2022

@author: olavg
"""

from board_state_format import board_state
from parse_board_state import parse_board_state
import copy
from is_card_play_legal import is_card_play_legal
import numpy as np


# test the outcome of a play without playing it (like playing it in your mind)
def test_play(player, my_pawns, other_pawns, hand):
    highest_board_value = 0
    test_player = copy.deepcopy(player)
    my_test_pawns = copy.deepcopy(my_pawns)
    other_test_pawns = copy.deepcopy(other_pawns)
    test_hand = copy.deepcopy(hand)
    move_value = 0
    secondary_pawn = 0
    card_plays_on_pawns_and_outcomes = []
    for card in test_hand:
        for my_pawn in my_test_pawns:
            my_other_test_pawns = [value for value in my_test_pawns if value != my_pawn]
            if card == 'A':
                if my_pawn.home:
                    my_pawn.home = False
                    my_pawn.position = 0
                else:
                    move_value = 1
                    my_pawn.position += 1
            if card == '2':
                move_value = 2
                if not my_pawn.home:
                    my_pawn.position += move_value
            if card == '3':
                move_value = 3
                if not my_pawn.home:
                    my_pawn.position += move_value
            if card == '4':
                move_value = -4
                if not my_pawn.home:
                    my_pawn.position += move_value

            # check if move is legal
            card_play_is_legal = is_card_play_legal(my_pawn, my_other_test_pawns, other_test_pawns, move_value)
            board_value = 3
            card_plays_on_pawns_and_outcomes.append({"card": card, "primary_pawn": my_pawn,
                                                     "secondary_pawn": secondary_pawn, "primary_move": move_value,
                                                     "card_play_is_legal": card_play_is_legal,
                                                     "board_value": board_value})

            # reset your mind game for the next iteration in the loop
            test_player = copy.deepcopy(player)
            my_test_pawns = copy.deepcopy(my_pawns)
            other_test_pawns = copy.deepcopy(other_pawns)
            test_hand = copy.deepcopy(hand)


if __name__ == '__main__':
    # This is the main executable that imports all classes to run a game

    # import and parse board state, return pawn objects, hand object, player object
    [player, my_pawns, other_pawns, hand, player_colors] = parse_board_state(board_state)
    player_count = len(player_colors)
    test_play(player, my_pawns, other_pawns, hand)

    bla = 1
"""
                if not move_is_legal(bla):
                    board_value = 0
                board_value = get_board_value()
                if board_value > highest_board_value:
                    highest_board_value = board_value
"""

"""
    # initiate a board_value matrix for every possible play
    board_value_of_all_plays = np.zeros((len(hand), len(my_pawns)))
    for card in hand:
        for pawn in my_pawns:
            for second_pawn in my_pawns + other_pawns:
                n = 1
                test_play_card_on_pawn_(card, pawn, second_pawn)
"""

    # For every card in hand, test-play the card on every pawn and find the new position
        # test if this is a legal move
        # calculate the board value
        # add the board value to the board_value overview

