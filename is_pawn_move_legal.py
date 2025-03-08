# checks for an illegal play
# TO DO
# jack_swap pawn at finish
# jack_swap pawn at position_0
# play card on pawn not on board


# move past board size

def play_jack_on_single_pawn(my_pawn):
    legal = True
    if my_pawn.position == None: # position is set to None in card_play_logic to trigger this
        legal = False
        my_pawn.position = 0    # This is necessary to prevent the other tests from failing
        return legal
    else:
        return legal


def move_past_board_size(my_pawn, game_info):
    legal = True
    if my_pawn.position >= game_info.board_size + 4:
        legal = False
        return legal
    else:
        return legal


def spawn_at_occupied_base(my_pawn, my_other_pawns):
    legal = True
    if my_pawn.position == 0 and not my_pawn.home and my_other_pawns:
        for my_other_pawn in my_other_pawns:
            if my_other_pawn.position == 0 and not my_other_pawn.home and not my_other_pawn.finish:
                legal = False
                return legal
            else:
                pass
        return legal
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
        if (other_pawn.is_protected and not other_pawn.home and
                (other_pawn.color == my_pawn.color or
                (not other_pawn.color == my_pawn.color and not other_pawn.finish))):
            # pass or hit a protected pawn while moving forward
            if my_pawn.position_at_start_of_turn < other_pawn.position <= my_pawn.position and move_value > 0:
                legal = False
                return legal
            # pass or hit a protected pawn (except own at 0) while moving backward
            elif my_pawn.position_at_start_of_turn > other_pawn.position >= my_pawn.position and move_value < 0:
                legal = False
                return legal
            # pass own pawn at 0 while moving backward
            elif other_pawn.position == 0 and my_pawn.position_at_start_of_turn < my_pawn.position and move_value < 0:
                legal = False
                return legal
            else:
                pass
        else:
            pass
    return legal


def move_back_out_from_finish(my_pawn, move_value, game_info):
    legal = True
    if (my_pawn.finish_at_start_of_turn and my_pawn.position - move_value > game_info.board_size - 1 and
            my_pawn.position < game_info.board_size):
        legal = False
        return legal
    else:
        return legal


# This function assumes that after a card play the target pawn is never at home. K and A put it on the board
# and all other card plays are illegal if the pawn is at home at start of turn
def play_card_on_pawn_at_home(my_pawn):
    legal = True
    if my_pawn.home:
        legal = False
        return legal
    else:
        return legal


def play_king_on_pawn_not_at_home(my_pawn):
    legal = True
    if my_pawn.home_at_start_of_turn == None:
        legal = False
        my_pawn.home_at_start_of_turn = False
        return legal
    else:
        return legal


def play_jack_on_protected_pawn(my_pawn, other_pawns):
    legal = True
    for other_pawn in other_pawns:
        if my_pawn.position == other_pawn.position_at_start_of_turn and \
                other_pawn.position == my_pawn.position_at_start_of_turn and \
                not my_pawn.home_at_start_of_turn and \
                not other_pawn.home_at_start_of_turn:
            if other_pawn.position_from_own_start_at_start_of_turn == 0 or my_pawn.position_at_start_of_turn == 0 or \
                    other_pawn.finish_at_start_of_turn or my_pawn.finish_at_start_of_turn:
                legal = False
                return legal
        else:
            pass
    return legal


def is_pawn_move_legal(my_pawn, my_other_pawns, other_pawns, move_value, game_info):
    legal_play_jack_on_single_pawn = play_jack_on_single_pawn(my_pawn)
    legal_move_past_board_size = move_past_board_size(my_pawn, game_info)
    legal_spawn = spawn_at_occupied_base(my_pawn, my_other_pawns)
    legal_move_past_protected_pawn = move_past_protected_pawn(my_pawn, my_other_pawns, other_pawns, move_value,
                                                              game_info)
    legal_move_back_out_from_finish = move_back_out_from_finish(my_pawn, move_value, game_info)
    legal_play_card_on_pawn_at_home = play_card_on_pawn_at_home(my_pawn)
    legal_play_king_on_pawn_not_at_home = play_king_on_pawn_not_at_home(my_pawn)
    legal_play_jack_on_protected_pawn = play_jack_on_protected_pawn(my_pawn, other_pawns)
    card_play_is_legal = (legal_play_jack_on_single_pawn and legal_move_past_board_size and legal_spawn and
                          legal_move_past_protected_pawn and legal_move_back_out_from_finish and
                          legal_play_card_on_pawn_at_home and legal_play_king_on_pawn_not_at_home and
                          legal_play_jack_on_protected_pawn)
    return card_play_is_legal
