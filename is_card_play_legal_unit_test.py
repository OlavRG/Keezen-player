# -*- coding: utf-8 -*-
"""
Created on Sun March 24 2024

@author: olavg
"""

import board_state_play_legality_unit_test as bs
from board_state_logic import parse_board_state
from card_play_logic import test_all_possible_plays


board_state_module_items = [f for f in bs.__dict__.items() if type(f[1]) == dict]
board_states_to_test = [g for g in board_state_module_items if 'pawns' in g[1]]

for board_state_tuple in board_states_to_test:
    print(board_state_tuple[0])
    board_state = board_state_tuple[1]
    [player, my_pawns, other_pawns, hand, game_info] = parse_board_state(board_state)
    turn_1_plays = test_all_possible_plays(player, my_pawns, other_pawns, hand, game_info)
    turn_1_legal_plays = [card_play for card_play in turn_1_plays if card_play[-1]["card_play_is_legal"]]

    # Use card history in board_state_play_legality_unit_test to write down the actual legal plays
    actual_legal_plays = board_state["card_history"].replace('A', '1').replace('Q', '0')
    """
    my_other_pawns = [value for value in my_pawns if value != my_pawns[0]]
    if other_pawns and hand[0].rank == 'J':
        target_pawn = other_pawns[0]
    elif my_other_pawns and hand[0].rank == '7':
        target_pawn = my_other_pawns[0]
    else:
        target_pawn = None
    card_plays_on_pawns_and_outcomes = []
    play_any_card_on_a_pawn_and_resolve_outcome(hand[0], my_pawns[0], my_other_pawns, other_pawns, game_info,
                                                card_plays_on_pawns_and_outcomes,
                                                target_pawn=target_pawn, move_1=None)
    """
    print(str(len(turn_1_legal_plays)) + "/" + actual_legal_plays + " legal plays detected")

bla=1