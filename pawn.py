
class Pawn():
    def __init__(self, color, position, position_from_own_start, home, finish, protected):
        self.color = color
        self.position = position
        self.position_from_own_start = position_from_own_start
        self.home = home
        self.finish = finish
        self.is_protected = protected

    def move(self, move_value):
        board_size = 64
        self.position += move_value
        if self.position > board_size - 1:
            self.finish = True
        elif self.position < 0:
            self.position = (self.position + board_size) % board_size
        else:
            pass
