
class Player:
    def __init__(self, color: str):
        self.color = color
        self.pawns = []
        self.hand = []
        # card_history should be reset everytime the deck is dealt
        self.card_history = ''
        self._hand_size = self.hand_size

    @property
    def hand_size(self):
        if self.hand:
            _hand_size = len(self.hand)
        else:
            _hand_size = 0
        return _hand_size

    @hand_size.setter
    def hand_size(self, value):
        _hand_size = value


class Players(list):
    def __init__(self):
        super().__init__()
        self._all_pawns = self.all_pawns

    @property
    def all_pawns(self):
        self._all_pawns = []
        for player in self:
            self._all_pawns.extend(player.pawns)
        return self._all_pawns

    def set_pawns_to_current_player_point_of_view(self, current_player, game_info):
        for player in self:
            for pawn in player.pawns:
                pawn.set_position_relative_to_current_player(current_player, game_info)

    def other_pawns(self, current_player):
        other_pawns = []
        for player in self:
            if player != current_player:
                other_pawns.extend(player.pawns)
        return other_pawns


"""
class Players:
    def __init__(self):
        self._all_players = []

    def __getitem__(self, index):
        return self._all_players[index]

    def __delitem__(self, index): 
        del self._all_players[index]

    def __len__(self):
        return len(self._all_players)

    def add_player(self, player: Player):
        self._all_players.append(player)

    def not_my_pawns(self, current_player):
        not_my_pawns = []
        return list(map(not_my_pawns.extend, [player.pawns for player in self._all_players if player != current_player]))
"""