# Checks for plays where the play is always illegal (like a J on a single pawn, or a 2-Q on a pawn with home==True)

def play_jack_on_single_pawn(card_play):
    legal = True
    if card_play["card"].swaps_pawns and (card_play["primary_pawn"] == False or card_play["secondary_pawn"] == False):
        legal = False
        return legal
    else:
        return legal


def play_jack_on_wrong_color_pawns(card_play, player):
    legal = True
    if card_play["card"].swaps_pawns and card_play["primary_pawn"].color == card_play["secondary_pawn"].color:
        legal = False
        return legal
    elif card_play["card"].swaps_pawns and \
        card_play["primary_pawn"].color != player.color and card_play["secondary_pawn"].color != player.color:
        legal = False
        return legal
    else:
        return legal


def play_jack_on_protected_pawn(card_play):
    legal = True
    if card_play["card"].swaps_pawns and (card_play["primary_pawn"].is_protected or card_play["secondary_pawn"].is_protected):
        legal = False
        return legal
    else:
        return legal


def play_jack_on_pawn_at_home(card_play):
    legal = True
    if card_play["card"].swaps_pawns and (card_play["primary_pawn"].home or card_play["secondary_pawn"].home):
        legal = False
        return legal
    else:
        return legal


def play_king_on_card_on_board(card_play):
    legal = True
    if card_play["card"].rank == "K" and card_play["primary_pawn"].home == False:
        legal = False
        return legal
    else:
        return legal


def play_card_on_pawn_at_home(card_play):
    legal = True
    if (card_play["primary_pawn"].home and card_play["card"].moves_pawn_from_home == False and
            not card_play["card"].rank == "A"):
        legal = False
        return legal
    else:
        return legal


def is_card_play_not_illegal_by_definition(card_play, player):
    legal_play_jack_on_single_pawn = play_jack_on_single_pawn(card_play)
    legal_play_jack_on_wrong_color_pawns = play_jack_on_wrong_color_pawns(card_play, player)
    legal_play_jack_on_protected_pawn = play_jack_on_protected_pawn(card_play)
    legal_play_jack_on_pawn_at_home = play_jack_on_pawn_at_home(card_play)
    legal_play_king_on_card_on_board = play_king_on_card_on_board(card_play)
    legal_play_card_on_pawn_at_home = play_card_on_pawn_at_home(card_play)

    card_play_is_not_illegal_by_definition = (legal_play_jack_on_single_pawn and
                                              legal_play_jack_on_wrong_color_pawns and
                                              legal_play_jack_on_protected_pawn and
                                              legal_play_jack_on_pawn_at_home and
                                              legal_play_king_on_card_on_board and
                                              legal_play_card_on_pawn_at_home)
    return card_play_is_not_illegal_by_definition
