
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
        self.is_protected = False

    def _check_for_finish(self, move_value, board_size):
        """
        This function is strictly for moving
        :param board_size: int
        """
        if move_value > 0 and self.position >= self.start_position:
            if self.position_at_start_of_turn < self.start_position:
                self.finish = True
                self.position = self.position % self.start_position
            elif self.position_at_start_of_turn + move_value != self.position: # additional requirement for pawns that
                # start past the start_position to run past the board_size and wrap around to move into the finish
                self.finish = True
                self.position = self.position % self.start_position
        else:
             pass    # pawn did not go into finish

        # move into finish
        if move_value > 0 and self.position >= board_size:
            if self.finish:
                self.finish_at_start_of_turn = True
            self.finish = True
            self.is_protected = True
        elif self.position < board_size:
            if self.finish:
                self.finish_at_start_of_turn = True
            self.finish = False
            self.is_protected = False
        elif move_value == 0:
            pass
        else:
            pass

    def _check_for_negative_position(self, board_size):
        if self.position < 0:
            self.position = (self.position + board_size) % board_size
        else:
            pass

    def _check_for_protection_from_own_0(self):
        if self.position == self.start_position:
            self.is_protected = True
        else:
            pass

    def _update_pawn_positions_by_move_value(self, move_value, board_size):
        self.position_at_start_of_turn = self.position
        self.position = (self.position + move_value) % board_size
        self._check_for_finish(move_value, board_size)
        self._check_for_negative_position(board_size)
        self._check_for_protection_from_own_0()

    def move_by_card(self, card, game_info, jack_other_pawn_position=None, move_from_7=None):
        if card.rank == 'A':
            if self.home:
                self.home_at_start_of_turn = self.home
                self.home = False
                self.position_at_start_of_turn = self.position
                self.position = self.start_position
                move_value = 0
                self._update_pawn_positions_by_move_value(move_value, game_info.board_size)
            else:
                move_value = 1
                self._update_pawn_positions_by_move_value(move_value, game_info.board_size)
        elif card.is_splittable:
            if move_from_7:
                move_value = move_from_7
            else:
                move_value = card.move_value
            self._update_pawn_positions_by_move_value(move_value, game_info.board_size)
        elif card.rank == 'J':
            self.position_at_start_of_turn = self.position
            self.position = jack_other_pawn_position
            self._update_pawn_positions_by_move_value(card.move_value, game_info.board_size)
        elif card.rank == 'K':
            if self.home:
                self.home_at_start_of_turn = self.home
                self.home = False
                self.position_at_start_of_turn = self.position
                self.position = 0
                self._update_pawn_positions_by_move_value(card.move_value, game_info.board_size)
            else:
                # This play would change nothing and is hence undetectable by is_card_play_legal. To detect the illegal
                # play, we set to None
                self.home_at_start_of_turn = None
        else:
            self._update_pawn_positions_by_move_value(card.move_value, game_info.board_size)
