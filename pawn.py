class Pawn:
    def __init__(self, color, position, start_position, home, finish, protected):
        self.color = color
        self.start_position = start_position    # position where this pawn spawns. Should be constant throughout a game
        self.position = position    # Absolute position (relative to start of first player in the game).
        self.position_at_start_of_turn = position
        self.home = home
        self.home_at_start_of_turn = home
        self.finish = finish
        self.finish_at_start_of_turn = finish
        self.is_protected = protected

    def __str__(self):
        return f'({self.color}, {self.position}, home: {self.home}, finish: {self.finish}, protected: {self.is_protected})'

    def reset_start_of_turn_bools_for_next_turn(self):
        self.position_at_start_of_turn = self.position
        self.home_at_start_of_turn = self.home
        self.finish_at_start_of_turn = self.finish

    def move_home(self):
        self.position_at_start_of_turn = self.position
        self.home_at_start_of_turn = self.home
        self.finish_at_start_of_turn = self.finish
        self.position = self.start_position
        self.home = True
        self.finish = False
        self._check_for_protection()

    def move_from_home_to_board(self):
        self.position_at_start_of_turn = self.position
        self.home_at_start_of_turn = self.home
        self.finish_at_start_of_turn = self.finish
        self.position = self.start_position
        self.home = False
        self.finish = False
        self._check_for_protection()

    def _check_for_protection(self):
        if (self.position == self.start_position and self.home == False) or self.finish:
            self.is_protected = True
        else:
            self.is_protected = False
            pass

    def move_by_increment(self, increment_is_positive: bool, board_size: int):
        if increment_is_positive:
            increment = 1
            self.position_at_start_of_turn = self.position
            self.position = (self.position + increment) % board_size
            if self.position == self.start_position:
                self.finish = True
                self.position = 0
            else:
                pass
        else:
            increment = -1
            self.position_at_start_of_turn = self.position
            if self.finish:
                self.position = (self.position + increment) # this way a 4 will give negative position in finish, which is illegal
            else:
                self.position = (self.position + increment) % board_size
        self._check_for_protection()

    def move_by_jack(self, new_position):
        self.position_at_start_of_turn = self.position
        self.position = new_position
        self._check_for_protection()
