
class Pawn():
    def __init__(self, color, position, position_from_own_start, home, finish, protected):
        self.color = color
        self.position = position
        self.position_from_own_start = position_from_own_start
        self.home = home
        self.finish = finish
        self.is_protected = protected

