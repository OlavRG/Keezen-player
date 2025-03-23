
class Player:
    def __init__(self, color: str):
        self.color = color
        self.pawns = []
        self.hand = []
        # card_history should be reset everytime the deck is dealt
        self.card_history = ''
        self._hand_size = self.hand_size # Hand size is annoying. Now you have to change this value every time a card is
        # played, discarded, or removed from the hand. And hand size is already known from self.hand!
        # New idea: scrap self.hand_size. Instead, add blind cards to players hands when creating another player from
        # a player PoV. Like Card('_'). This mirrors real life, where you see actual cards, but do not know their rank.

    @property
    def hand_size(self):
        return len(self.hand)

    @hand_size.setter
    def hand_size(self, value):
        self._hand_size = value


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
