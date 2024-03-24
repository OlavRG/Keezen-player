
class GameInfo:
    def __init__(self, player_colors):
        self.player_colors = player_colors
        self.player_count = len(player_colors)
        self.board_size = 16*self.player_count
