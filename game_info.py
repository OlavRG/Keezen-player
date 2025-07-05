
class GameInfo:
    def __init__(self, player_colors_in_start_order, player_colors_in_round_order):
        """

        :param player_colors:
        """
        self.player_colors_in_start_order = player_colors_in_start_order   # First round turn order. Used to determine board position 0
        self.player_colors_in_round_order = player_colors_in_round_order   # Current round order. Changes with every deck-shuffle
        self.player_count = len(player_colors_in_start_order)
        self.pawns_per_player = 4
        self.board_size_per_player = 16
        self.board_size = self.board_size_per_player * self.player_count
