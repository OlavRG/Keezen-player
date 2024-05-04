board_state = {"pawns": [
     {"color":"Orange","position":30,"home":False,"finish":False},
     {"color":"Orange","position":25,"home":False,"finish":False},
     {"color": "Red", "position": 1, "home": False, "finish": False}],
    "hand": 'X5K',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }

"""
# test no going backwards over own protected pawn
board_state = {"pawns": [
     {"color":"Orange","position":0,"home":False,"finish":False},
     {"color":"Orange","position":1,"home":False,"finish":False}],
    "hand": '4',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }
"""

# Test spawn at occupied base
"""
board_state = {"pawns": [
     {"color":"Orange","position":0,"home":True,"finish":False},
     {"color":"Orange","position":0,"home":False,"finish":False}],
    "hand": 'K',
    "other_hands": [5, 5, 5],
    "my_color": "Orange",
    "card_history": ""
    }
"""


board_state_start = {"pawns": [
     {"color":"Blue","position":0,"home":True,"finish":False},
     {"color":"Blue","position":1,"home":True,"finish":False},
     {"color":"Blue","position":2,"home":True,"finish":False},
     {"color":"Blue","position":3,"home":True,"finish":False},
     {"color":"Orange","position":0,"home":True,"finish":False},
     {"color":"Orange","position":1,"home":True,"finish":False},
     {"color":"Orange","position":2,"home":True,"finish":False},
     {"color":"Orange","position":3,"home":True,"finish":False},
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


print (board_state["pawns"])
