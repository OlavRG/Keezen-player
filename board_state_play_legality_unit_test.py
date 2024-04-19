# Several board states are given to test if the legality check works correctly.
# For each given board state the card play on the first pawn of my_color is the check.


# test not to exceed board size. Should return False
board_state_move_past_board_size = {"pawns": [
     {"color":"Blue","position":0,"home":True,"finish":False},
     {"color":"Orange","position":60,"home":False,"finish":False},
     {"color":"Red","position":0,"home":True,"finish":False},
     {"color":"White","position":0,"home":True,"finish":False}],
    "hand": 'Q',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# test if we can move past opponent protected pawn. Should return False
board_state_move_forward_past_opponent_protected_pawn = {"pawns": [
     {"color":"Blue","position":0,"home":False,"finish":False},
     {"color":"Orange","position":8,"home":False,"finish":False},
     {"color":"Red","position":0,"home":False,"finish":False},
     {"color":"White","position":0,"home":False,"finish":False}],
    "hand": 'Q',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# test if we can move past opponent protected pawn. Should return False
board_state_move_backward_past_opponent_protected_pawn = {"pawns": [
     {"color":"Blue","position":0,"home":False,"finish":False},
     {"color":"Orange","position":18,"home":False,"finish":False},
     {"color":"Red","position":0,"home":False,"finish":False},
     {"color":"White","position":0,"home":False,"finish":False}],
    "hand": '4',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# test no going backwards over own protected pawn. Should return False
board_state_move_back_over_own_protected_pawn = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":False},
     {"color":"Orange","position":0,"home":False,"finish":False}],
    "hand": '4',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test move past own pawn in finish. Should return False
board_state_move_past_own_pawn_in_finish = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":True},
     {"color":"Orange","position":2,"home":False,"finish":True}],
    "hand": '2',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test move backwards out of finish. Should return False
board_state_move_back_out_of_finish = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":True}],
    "hand": '4',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test spawn at occupied base. Should return False
board_state_spawn_at_occupied_base = {"pawns": [
     {"color":"Orange","position":0,"home":True,"finish":False},
     {"color":"Orange","position":0,"home":False,"finish":False}],
    "hand": 'A',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test card play with no pawns on the board when card is not a K or A, but regular move card. Should return False
board_state_play_move_card_with_no_pawn_on_board = {"pawns": [
     {"color":"Orange","position":0,"home":True,"finish":False}],
    "hand": '6',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test play jack with own pawn not on board. Should return False
board_state_no_own_pawn_on_board_play_jack = {"pawns": [
     {"color":"Blue","position":1,"home":False,"finish":False},
     {"color":"Orange","position":1,"home":True,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test play jack on own 2 pawns. Should return False
board_state_play_jack_on_own_pawns = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":False},
     {"color":"Orange","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test play jack with only 1 pawn on board. Should return False
board_state_play_jack_on_single_pawn = {"pawns": [
     {"color":"Orange","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test play jack on own pawn at position_0. Should return False
board_state_play_jack_on_own_pawn_at_0 = {"pawns": [
     {"color":"Orange","position":0,"home":False,"finish":False},
     {"color":"Blue","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test play jack on own pawn at finish. Should return False
board_state_play_jack_on_own_pawn_at_finish = {"pawns": [
     {"color":"Orange","position":1,"home":False,"finish":True},
     {"color":"Blue","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test play jack on opponent pawn at their position_0. Should return False
board_state_play_jack_on_opponent_pawn_at_0 = {"pawns": [
     {"color":"Blue","position":0,"home":False,"finish":False},
     {"color":"Orange","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }


# Test play jack on opponent pawn at their finish. Should return False
board_state_play_jack_on_opponent_finished_pawn = {"pawns": [
     {"color":"Blue","position":1,"home":False,"finish":True},
     {"color":"Orange","position":2,"home":False,"finish":False}],
    "hand": 'J',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }

# Test play king on pawn not at home. Should return False
board_state_play_king_on_pawn_not_at_home = {"pawns": [
     {"color":"Blue","position":1,"home":False,"finish":True},
     {"color":"Orange","position":0,"home":False,"finish":False}],
    "hand": 'K',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
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
"""

