# -*- coding: utf-8 -*-
"""
Created on Sun March 24 2024

@author: olavg
"""

import board_state_play_legality_unit_test as bs
from parse_board_state import parse_board_state
from card_play_logic import play_any_card_on_a_pawn_and_resolve_outcome

board_state_module_items = [f for f in bs.__dict__.items() if type(f[1]) == dict]
board_states_to_test = [g for g in board_state_module_items if 'pawns' in g[1]]

for board_state_tuple in board_states_to_test:
    print(board_state_tuple[0])
    board_state = board_state_tuple[1]
    [player, my_pawns, other_pawns, hand, game_info] = parse_board_state(board_state)
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
                                                target_pawn=None, move_1=None)

    print(card_plays_on_pawns_and_outcomes[0][0]["card_play_is_legal"])

bla=1