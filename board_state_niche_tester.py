
# This file contains board states that have not-straight forward plays, ones which are difficult for a computer

# Best play: 3, 3, hand afleggen. Tijd rekken als je voor een geblokkeerde pion staat.
board_state_blocked = {"pawns": [
     {"color":"Orange","position": 8, "home": False,"finish": False},
     {"color": "Red", "position": 0, "home": False, "finish": False}],
    "hand": '337',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }

# Best play: X. Zeker weten dat hij direct de finish in loopt ookal is er geen vervolg zet.
board_state_walk_into_finish_without_follow_up_move = {"pawns": [
     {"color":"Orange","position": 25, "home": False,"finish": False},
     {"color": "Red", "position": 0, "home": False, "finish": False}],
    "hand": 'X33',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }