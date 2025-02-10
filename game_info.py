
class GameInfo:
    def __init__(self, player_colors):
        self.player_colors_in_turn_order = player_colors
        self.player_count = len(player_colors)
        self.board_size_per_player = 16
        self.board_size = self.board_size_per_player * self.player_count

