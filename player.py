
class Player:
    def __init__(self, color: str):
        self.color = color
        self.pawns = []
        self.hand = []
        # card_history should be reset everytime the deck is dealt
        self.card_history = ''

    """
    @property
    def hand_size(self):
        return self._hand_size

    @hand_size.setter
    def hand_size(self, value):
        self._hand_size = value
    """

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

    def other_pawns(self, current_player):
        other_pawns = []
        for player in self:
            if player != current_player:
                other_pawns.extend(player.pawns)
        return other_pawns
