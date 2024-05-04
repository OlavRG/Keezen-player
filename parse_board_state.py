import copy

from player import Player
from card import Card
from pawn import Pawn
from game_info import GameInfo
import random

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


def create_starting_board_state(n_players):
    # currently 8 colors and hence 8 players are supported
    colors = ['red', 'white', 'blue', 'orange', 'black', 'green', 'magenta', 'cyan']
    board_states_start = [{} for iterator in range(0, n_players)]
    deck = list(n_players * 'A23456789XJQK')
    random.shuffle(deck)
    hands = [[] for iterator in range(0,n_players)]
    pawns = []
    for player in range(0,n_players):
        hands[player].append(deck.pop())
        hands[player].append(deck.pop())
        hands[player].append(deck.pop())
        hands[player].append(deck.pop())
        hands[player].append(deck.pop())
        board_states_start[player]["hand"] = ''.join(hands[player])
        board_states_start[player]["other_hands"] = [5] * (n_players - 1)
        board_states_start[player]["my_color"] = colors[player]
        board_states_start[player]["card_history"] = ""
        pawns.append({"color": colors[player], "position": 0, "home": True, "finish": False})
        pawns.append({"color": colors[player], "position": 1, "home": True, "finish": False})
        pawns.append({"color": colors[player], "position": 2, "home": True, "finish": False})
        pawns.append({"color": colors[player], "position": 3, "home": True, "finish": False})
        board_states_start[player]["pawns"] = pawns

    return board_states_start

bla = create_starting_board_state(6)

bla =1