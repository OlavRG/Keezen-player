# FUNCTION:
#   This script contains all functions that let the server set up the game objects (players, pawns, deck, discard_pile,
#   and player.hand) for a game to start. It also contains all functions for the client to set up the game objects from
#   their perspective.
#   Secondly it makes the board_state dictionary that is used to communicate all relevant info from the server to the
#   clients, and to convert game objects to this board_state and vice versa.

from player import Player
from card import Card
from pawn import Pawn
from game_info import GameInfo
import random


def create_game_objects_from_board_state(board_state):
    player = Player(board_state["my_color"])
    for card in board_state["hand"]:
        player.hand.append(Card(card))
    # get unique colors with same order as board_state. This determines player order!
    player_colors = []
    for pawn in board_state["pawns"]:
        if pawn["color"] not in player_colors:
            player_colors.append(pawn["color"])
    player.card_history = ''.join(player_history["card_history"] for player_history in board_state["card_history"] if
                                  player_history["color"] == player.color)
    game_info = GameInfo(player_colors)
    discard_pile_card_string = ''.join(player_history["card_history"] for player_history in board_state["card_history"])
    discard_pile = [Card(card) for card in discard_pile_card_string]
    other_pawns = []
    for pawn in board_state["pawns"]:
        if pawn["position"] == 0 or pawn["finish"]:
            is_protected = True
        else:
            is_protected = False
        if pawn["color"] == player.color:
            if pawn["finish"] and pawn["position"] in range(0, 4):
                pawn["position"] = pawn["position"] + game_info.board_size
            player.pawns.append(Pawn(pawn["color"], pawn["position"], pawn["position"],
                                pawn["home"], pawn["finish"], is_protected))
        elif pawn["color"] != player.color:
            pawn_turn_relative_to_player = ((player_colors.index(pawn["color"]) - player_colors.index(player.color)) %
                                            len(player_colors))
            position_relative_to_player_start = pawn["position"] + 16 * pawn_turn_relative_to_player
            position_relative_to_player_start = position_relative_to_player_start % game_info.board_size
            other_pawns.append(Pawn(pawn["color"], position_relative_to_player_start, pawn["position"],
                                    pawn["home"], pawn["finish"], is_protected))
    return player, other_pawns, discard_pile, game_info


def set_pawns_to_current_player_PoV(players, current_player, game_info):
    other_pawns = []
    list(map(other_pawns.extend, [player.pawns for player in players if player != current_player]))
    for pawn in current_player.pawns + other_pawns:
        pawn.set_position_relative_to_current_player(current_player, game_info)
    return other_pawns


def deal_cards_from_deck_to_players(players, deck, cards_per_player):
    for player in range(len(players)):
        for card in range(cards_per_player):
            players[player].hand.append(deck.pop())


def create_starting_game_objects(n_players):
    # currently 8 colors and hence 8 players are supported
    colors = ['red', 'white', 'blue', 'orange', 'black', 'green', 'magenta', 'cyan']
    if n_players > len(colors):
        raise ValueError("Number of players cannot be greater than 8. Currently only 8 player colors are defined.")
    game_info = GameInfo(colors[:n_players])
    deck = list(map(Card, list(n_players * 'A23456789XJQK')))
    random.shuffle(deck)
    discard_pile = []
    players = []
    for player in range(0, n_players):
        players.append(Player(colors[player]))
        players[player].pawns.append(Pawn(colors[player], 0, 0, home=True, finish=False, protected=True))
        players[player].pawns.append(Pawn(colors[player], 0, 0, home=True, finish=False, protected=True))
        players[player].pawns.append(Pawn(colors[player], 0, 0, home=True, finish=False, protected=True))
        players[player].pawns.append(Pawn(colors[player], 0, 0, home=True, finish=False, protected=True))

    return players, deck, discard_pile, game_info


def create_board_states_per_client(players, deck, game_info):
    board_states = [{} for iterator in range(0, len(players))]
    hands = [[] for iterator in range(0, len(players))]
    other_hands_size = [[] for iterator in range(0, len(players))]
    pawns = []
    card_history = []
    for n_player in range(0, len(players)):
        hands[n_player] = ''.join(card.rank for card in players[n_player].hand)
        board_states[n_player]["hand"] = hands[n_player]
        other_hands_size[n_player] = [len(any_player.hand) for any_player in players if any_player != players[n_player]]
        board_states[n_player]["other_hands"] = other_hands_size[n_player]
        board_states[n_player]["my_color"] = players[n_player].color
        card_history.append({"color": players[n_player].color, "card_history": players[n_player].card_history})
        board_states[n_player]["card_history"] = card_history
        for pawn in players[n_player].pawns:
            pawns.append({"color": pawn.color, "position": pawn.position_from_own_start % game_info.board_size,
                          "home": pawn.home, "finish": pawn.finish})
        board_states[n_player]["pawns"] = pawns

    # next: cards left in deck should be added to board state format
    return board_states


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
    "card_history": [
        {"color": "Blue", "card_history": '483JX'},
        {"color": "Orange", "card_history": '483JX'},
        {"color": "Red", "card_history": '483JX'},
        {"color": "White", "card_history": '483JX'}]
    }


"""
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
"""



bla =1