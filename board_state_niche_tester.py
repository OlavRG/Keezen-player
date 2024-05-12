
# This file contains board states that have not-straight forward plays, ones which are difficult for a computer

# Best play: 3, 3, hand afleggen. Tijd rekken als je voor een geblokkeerde pion staat.
board_state_blocked = {"pawns": [
     {"color":"Orange","position": 8, "home": False,"finish": False},
     {"color": "Red", "position": 0, "home": False, "finish": False}],
    "hand": '267',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }

# Best play: X. Zeker weten dat hij direct de finish in loopt ookal is er geen vervolg zet.
board_state_walk_last_pawn_into_finish = {"pawns": [
     {"color":"Orange","position": 25, "home": False,"finish": False},
     {"color": "Red", "position": 0, "home": False, "finish": False}],
    "hand": 'X33',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }

board_state_walk_backwards_and_into_finish = {"pawns": [
     {"color":"Orange","position": 0, "home": True,"finish": False},
     {"color": "Red", "position": 0, "home": False, "finish": False}],
    "hand": 'K468',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }
