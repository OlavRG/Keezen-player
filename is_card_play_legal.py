# checks for an illegal play
# TO DO
# jack_swap pawn at finish
# jack_swap pawn at position_0
# play card on pawn not on board
# move past board size


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
#   pass pawn at position_0
#   hit pawn at position_0
def move_past_protected_pawn(my_pawn, my_other_pawns, other_pawns, move_value):
    legal = True
    for other_pawn in my_other_pawns + other_pawns:
        if not other_pawn.is_protected:
            return legal
        else:
            # pass a protected pawn while moving forward
            if my_pawn.position < other_pawn.position <= my_pawn.position+move_value:
                legal = False
                return legal
            # pass a protected pawn while moving backward with a 4
            elif my_pawn.position > other_pawn.position >= my_pawn.position+move_value:
                legal = False
                return legal
            else:
                return legal


def is_card_play_legal(my_pawn, my_other_pawns, other_pawns, move_value):
    legal_spawn = spawn_at_occupied_base(my_pawn, my_other_pawns)
    legal_move_past_protected_pawn = move_past_protected_pawn(my_pawn, my_other_pawns, other_pawns, move_value)
    card_play_is_legal = legal_spawn and legal_move_past_protected_pawn
    return card_play_is_legal
