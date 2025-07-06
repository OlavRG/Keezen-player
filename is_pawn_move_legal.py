# checks for an illegal play
# TO DO
# jack_swap pawn at finish
# jack_swap pawn at position_0
# play card on pawn not on board


def move_outside_finish_position(my_pawn, game_info):
    legal = True
    if my_pawn.finish and not (game_info.pawns_per_player > my_pawn.position >= 0):
        legal = False
        return legal
    else:
        return legal


def move_onto_protected_pawn(my_pawn, players):
    legal = True
    all_other_pawns = [pawn for pawn in players.all_pawns if pawn != my_pawn]
    for other_pawn in all_other_pawns:
        if (my_pawn.position == other_pawn.position and
                my_pawn.home == other_pawn.home == False and
                other_pawn.is_protected):
            if my_pawn.finish == False and other_pawn.finish == False: # look for pawns on the board outside finish
                legal = False
                return legal
            elif my_pawn.finish == True and other_pawn.finish == True and other_pawn.color == my_pawn.color:
                legal = False
                return legal
            else:
                pass
        else:
            pass
    return legal


def is_move_by_jack_legal(pawn):
    move_by_jack_is_legal = not pawn.is_protected
    return move_by_jack_is_legal


def is_pawn_move_legal(my_pawn, players, game_info):
    legal_move_outside_finish_position = move_outside_finish_position(my_pawn, game_info)
    legal_move_onto_protected_pawn = move_onto_protected_pawn(my_pawn, players)
    pawn_move_is_legal = (legal_move_outside_finish_position and legal_move_onto_protected_pawn)
    return pawn_move_is_legal