# -*- coding: utf-8 -*-
"""
Created on Sun March 24 2024

@author: olavg
"""

import board_state_play_legality_unit_test as bs
from parse_board_state import parse_board_state
from is_card_play_legal import is_card_play_legal

[player, my_pawns, other_pawns, hand, game_info] = parse_board_state(bs.board_state_move_past_board_size)
for my_pawn in my_pawns:
    my_other_pawns = [value for value in my_pawns if value != my_pawn]
    card_play_is_legal = is_card_play_legal(my_pawn, my_other_pawns, other_pawns, move_value, game_info)

