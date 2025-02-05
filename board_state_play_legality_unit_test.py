# This file provides the input for is_card_play_legal_unit_test.
# Each board state should be accompanied by a card play and if it is expected to be legal.

# TO DO:
# - add card play dicts and expected legality. Assemble in some logical format (dict?)
# - Maybe rename this file and change to filetype (.json maybe?)


# test if you can hit your own pawn that started turn at home. Should be legal. It is easy for a legality checker
# to say that any pawn that starts its turn at home cannot be tackled the same turn.
board_state_tackle_own_pawn_that_started_at_home = {"pawns": [
     {"color":"red","position":0,"home":False,"finish":False},
     {"color":"red","position":1,"home":False,"finish":False}],
    "hand": '7',
    "other_hands": [5, 5, 5],
    "my_color": "Red",
    "card_history": ""
    }

card_play_dict = {"card": "7",
                  "primary_pawn_color": "red",
                  "primary_pawn_position": 0,
                  "primary_pawn_home": False,
                  "primary_pawn_finish": False,
                  "secondary_pawn_color": "red",
                  "secondary_pawn_position": 1,
                  "secondary_pawn_home": False,
                  "secondary_pawn_finish": False,
                  "primary_move": 4}

is_legal_expected = True


# test not to exceed board size. 
board_state_move_past_board_size = {"pawns": [
     {"color":"Blue","position":0,"home":True,"finish":False},
     {"color":"Orange","position":60,"home":False,"finish":False},
     {"color":"Red","position":0,"home":True,"finish":False},
     {"color":"White","position":0,"home":True,"finish":False}],
    "hand": 'Q',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# test if we can move past opponent protected pawn. 
board_state_move_forward_past_opponent_protected_pawn = {"pawns": [
     {"color":"Blue","position":0,"home":False,"finish":False},
     {"color":"Orange","position":8,"home":False,"finish":False},
     {"color":"Red","position":0,"home":False,"finish":False},
     {"color":"White","position":0,"home":False,"finish":False}],
    "hand": 'Q',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# test if we can move past opponent protected pawn. 
board_state_move_backward_past_opponent_protected_pawn = {"pawns": [
     {"color":"Blue","position":0,"home":False,"finish":False},
     {"color":"Orange","position":18,"home":False,"finish":False},
     {"color":"Red","position":0,"home":False,"finish":False},
     {"color":"White","position":0,"home":False,"finish":False}],
    "hand": '4',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# test no going backwards over own protected pawn. 
board_state_move_back_over_own_protected_pawn = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":False},
     {"color":"Orange","position":0,"home":False,"finish":False}],
    "hand": '4',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "A"
    }


# Test move past own pawn in finish. 
board_state_move_past_own_pawn_in_finish = {"pawns": [
     {"color":"Orange","position":0,"home":False,"finish":True},
     {"color":"Orange","position":1,"home":False,"finish":True}],
    "hand": '2',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "A"
    }


# Test move backwards out of finish. 
board_state_move_back_out_of_finish = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":True}],
    "hand": '4',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# Test spawn at occupied base. 
board_state_spawn_at_occupied_base = {"pawns": [
     {"color":"Orange","position":0,"home":True,"finish":False},
     {"color":"Orange","position":0,"home":False,"finish":False}],
    "hand": 'A',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "A"
    }


# Test card play with no pawns on the board when card is not a K or A, but regular move card. 
board_state_play_move_card_with_no_pawn_on_board = {"pawns": [
     {"color":"Orange","position":0,"home":True,"finish":False}],
    "hand": '6',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# Test play jack with own pawn not on board. 
board_state_no_own_pawn_on_board_play_jack = {"pawns": [
     {"color":"Blue","position":1,"home":False,"finish":False},
     {"color":"Orange","position":1,"home":True,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# Test play jack on own 2 pawns. 
board_state_play_jack_on_own_pawns = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":False},
     {"color":"Orange","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# Test play jack with only 1 pawn on board. 
board_state_play_jack_on_single_pawn = {"pawns": [
     {"color":"Orange","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# Test play jack on own pawn at position_0. 
board_state_play_jack_on_own_pawn_at_0 = {"pawns": [
     {"color":"Orange","position":0,"home":False,"finish":False},
     {"color":"Blue","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# Test play jack on own pawn at finish. 
board_state_play_jack_on_own_pawn_at_finish = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":True},
     {"color":"Blue","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# Test play jack on opponent pawn at their position_0. 
board_state_play_jack_on_opponent_pawn_at_0 = {"pawns": [
     {"color":"Blue","position":0,"home":False,"finish":False},
     {"color":"Orange","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }


# Test play jack on opponent pawn at their finish. 
board_state_play_jack_on_opponent_finished_pawn = {"pawns": [
     {"color":"Blue","position":1,"home":False,"finish":True},
     {"color":"Orange","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }

# Test play king on pawn not at home. 
board_state_play_king_on_pawn_not_at_home = {"pawns": [
     {"color":"Blue","position":1,"home":False,"finish":True},
     {"color":"Orange","position":0,"home":False,"finish":False}],
    "hand": 'K',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "Q"
    }

# Test if a legal jack move (orange 1 with blue 8) doesn't trigger any illegality checks.
board_state_move_with_Jack_with_legal_target_pawn_while_protected_pawns_are_on_board = {"pawns": [
     {"color":"Blue","position":8,"home":False,"finish":False},
     {"color":"Blue","position":0,"home":False,"finish":False},
     {"color":"Orange","position":0,"home":False,"finish":False},
     {"color":"Orange","position":1,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": "A"
    }


""""
board_state = {"pawns": [
     {"color":"Blue","position":0,"home":True,"finish":False},
     {"color":"Blue","position":1,"home":True,"finish":False},
     {"color":"Blue","position":2,"home":True,"finish":False},
     {"color":"Blue","position":3,"home":True,"finish":False},
     {"color":"Orange","position":0,"home":True,"finish":False},
     {"color":"Orange","position":1,"home":False,"finish":False},
     {"color":"Orange","position":2,"home":True,"finish":False},
     {"color":"Orange","position":0,"home":False,"finish":False},
     {"color":"Red","position":0,"home":True,"finish":False},
     {"color":"Red","position":1,"home":True,"finish":False},
     {"color":"Red","position":2,"home":True,"finish":False},
     {"color":"Red","position":3,"home":True,"finish":False},
     {"color":"White","position":0,"home":True,"finish":False},
     {"color":"White","position":1,"home":True,"finish":False},
     {"color":"White","position":2,"home":True,"finish":False},
     {"color":"White","position":3,"home":True,"finish":False}],
    "hand": 'A47JQ',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }

    card_play_dict = {"card": card_play["card"].rank,
                      "primary_pawn_color": card_play["primary_pawn"].color,
                      "primary_pawn_position": card_play["primary_pawn"].position_from_own_start,
                      "primary_pawn_home": card_play["primary_pawn"].home,
                      "primary_pawn_finish": card_play["primary_pawn"].finish,
                      "secondary_pawn_color": secondary_pawn_color,
                      "secondary_pawn_position": secondary_pawn_position_from_own_start,
                      "secondary_pawn_home": secondary_pawn_home,
                      "secondary_pawn_finish": secondary_pawn_finish,
                      "primary_move": card_play["primary_move"]}
"""

