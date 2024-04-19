
from player import Player
from card import Card
from pawn import Pawn
from game_info import GameInfo

def parse_board_state(board_state):
    player = Player(board_state["my_color"])
    hand = []
    for card in board_state["hand"]:
        hand.append(Card(card))
    # get unique colors with same order as board_state. This determines player order!
    player_colors = []
    for pawn in board_state["pawns"]:
        if pawn["color"] not in player_colors:
            player_colors.append(pawn["color"])
    game_info = GameInfo(player_colors)
    my_pawns = []
    other_pawns = []
    for pawn in board_state["pawns"]:
        if pawn["position"] == 0 or pawn["finish"]:
            is_protected = True
        else:
            is_protected = False
        if pawn["color"] == player.color:
            if pawn["finish"] and pawn["position"] in range(0, 4):
                pawn["position"] = pawn["position"] + game_info.board_size
            my_pawns.append(Pawn(pawn["color"], pawn["position"], pawn["position"],
                                 pawn["home"], pawn["finish"], is_protected))
        elif pawn["color"] != player.color:
            pawn_turn_relative_to_player = player_colors.index(pawn["color"]) - player_colors.index(player.color)
            if pawn_turn_relative_to_player < 0:
                pawn_turn_relative_to_player = pawn_turn_relative_to_player + len(player_colors)
            position_relative_to_player_start = pawn["position"] + 16 * pawn_turn_relative_to_player
            position_relative_to_player_start = ((position_relative_to_player_start + game_info.board_size)
                                                 % game_info.board_size)
            other_pawns.append(Pawn(pawn["color"], position_relative_to_player_start, pawn["position"],
                                    pawn["home"], pawn["finish"], is_protected))
    return player, my_pawns, other_pawns, hand, game_info

