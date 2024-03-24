# checks for an illegal play
# TO DO
# jack_swap pawn at finish
# jack_swap pawn at position_0
# play card on pawn not on board


# move past board size
def move_past_board_size(my_pawn, game_info):
    legal = True
    if my_pawn.position > game_info.board_size + 4:
        legal = False
        return legal
    else:
        return legal


def spawn_at_occupied_base(my_pawn, my_other_pawns):
    legal = True
    if my_pawn.position == 0 and not my_pawn.home:
        for my_other_pawn in my_other_pawns:
            if my_other_pawn.position == 0 and not my_other_pawn.home:
                legal = False
                return legal
            else:
                pass
    else:
        return legal


# This function solves various issues:
#   hit pawn at finish
#   pass pawn at finish
#   pass pawn at their start
#   pass pawn at position_0
#   hit pawn at
def move_past_protected_pawn(my_pawn, my_other_pawns, other_pawns, move_value, game_info):
    legal = True
    for other_pawn in my_other_pawns + other_pawns:
        if not other_pawn.is_protected:
            return legal
        else:
            # pass or hit a protected pawn while moving forward
            if my_pawn.previous_position < other_pawn.position <= my_pawn.position:
                legal = False
                return legal
            # pass or hit a protected pawn (except own at 0) while moving backward
            elif my_pawn.previous_position > other_pawn.position >= my_pawn.position:
                legal = False
                return legal
            # pass own pawn at 0 while moving backward
            elif other_pawn.position == 0 and my_pawn.previous_position < my_pawn.position and move_value < 0:
                legal = False
                return legal
            else:
                return legal


def move_back_out_from_finish(my_pawn, move_value, game_info):
    legal = True
    if my_pawn.previously_in_finish and my_pawn.position - move_value > game_info.board_size - 1 and my_pawn.position <= game_info.board_size:
        legal = False
        return legal
    else:
        return legal


def is_card_play_legal(my_pawn, my_other_pawns, other_pawns, move_value, game_info):
    legal_move_past_board_size = move_past_board_size(my_pawn, game_info)
    legal_spawn = spawn_at_occupied_base(my_pawn, my_other_pawns)
    legal_move_past_protected_pawn = move_past_protected_pawn(my_pawn, my_other_pawns, other_pawns, move_value,
                                                              game_info)
    legal_move_back_out_from_finish = move_back_out_from_finish(my_pawn, move_value, game_info)
    card_play_is_legal = (legal_move_past_board_size and legal_spawn and legal_move_past_protected_pawn and
                          legal_move_back_out_from_finish)
    return card_play_is_legal
