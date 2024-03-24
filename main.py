# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 11:22:10 2022

@author: olavg
"""

from board_state_format import board_state
from parse_board_state import parse_board_state
import copy
from is_card_play_legal import is_card_play_legal


# test the outcome of a play without playing it (like playing it in your mind)
def test_all_possible_plays(player, my_pawns, other_pawns, hand, game_info):
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
            if card is '7':
                for my_other_test_pawn in my_other_test_pawns:
                    for move_1 in range(0,8):
                        move_2 = 7 - move_1
                        my_pawn.play_card_on_pawn(card, game_info, move_from_7 = move_1)
                        my_other_test_pawn.play_card_on_pawn(card, game_info, move_from_7 = move_2)
            elif card is 'J':
                for other_test_pawn in other_test_pawns:
                    position_1 = my_pawn.position
                    position_2 = other_test_pawn.position
                    my_pawn.play_card_on_pawn(card, game_info, jack_other_pawn_position=position_2)
                    other_test_pawn.play_card_on_pawn(card, game_info, jack_other_pawn_position=position_1)
            else:
                my_pawn.play_card_on_pawn(card, game_info)

            # check if move is legal
            card_play_is_legal = is_card_play_legal(my_pawn, my_other_test_pawns, other_test_pawns, move_value,
                                                    game_info)
            # get board value
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
    return card_plays_on_pawns_and_outcomes

if __name__ == '__main__':
    # This is the main executable that imports all classes to run a game

    # import and parse board state, return pawn objects, hand object, player object
    [player, my_pawns, other_pawns, hand, game_info] = parse_board_state(board_state)
    card_plays_on_pawns_and_outcomes = test_play(player, my_pawns, other_pawns, hand, game_info)

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

