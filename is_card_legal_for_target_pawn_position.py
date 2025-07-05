# Checks for plays where the play is always illegal (like a J on a single pawn, or a 2-Q on a pawn with home==True)

def play_jack_on_single_pawn(card_play):
    legal = True
    if card_play["card"].rank == "J" and (card_play["primary_pawn"] == False or card_play["secondary_pawn"] == False):
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


# This function assumes that after a card play the target pawn is never at home. K and A put it on the board
# and all other card plays are illegal if the pawn is at home at start of turn
def play_card_on_pawn_at_home(my_pawn):
    legal = True
    if my_pawn.home:
        legal = False
        return legal
    else:
        return legal


def is_card_legal_for_target_pawn_position(card_play):
    legal_play_jack_on_single_pawn = play_jack_on_single_pawn(card_play)
    legal_play_king_on_card_on_board = play_king_on_card_on_board(card_play)

    card_is_legal_for_target_pawn_position = (legal_play_jack_on_single_pawn and legal_play_king_on_card_on_board)
    return card_is_legal_for_target_pawn_position

"""
bla =  {"card": card, "primary_pawn": my_pawn,
        "secondary_pawn": target_pawn, "primary_move": move_value,
        "card_play_is_legal": card_play_is_legal,
        "board_value": board_value}
"""