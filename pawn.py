
class Pawn:
    def __init__(self, color, position, start_position, home, finish, protected):
        self.color = color
        self.start_position = start_position
        self.position = position    # position relative to start of first player in the game
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
        self.position = 0
        self.home = True
        self.finish = False
        self.finish_at_start_of_turn = False
        self.is_protected = False

    def _check_for_finish(self, board_size):
        if self.position >= board_size:
            if self.finish:
                self.finish_at_start_of_turn = True
            self.finish = True
            self.is_protected = True
        elif self.position < board_size:
            if self.finish:
                self.finish_at_start_of_turn = True
            self.finish = False
            self.is_protected = False
        else:
            pass

    def _check_for_negative_position(self, board_size):
        if self.position < 0 or self.position_from_own_start < 0:
            self.position = (self.position + board_size) % board_size
            self.position_from_own_start = (self.position_from_own_start + board_size) % board_size
            self.is_protected = False
        else:
            pass

    def _check_for_protection_from_own_0(self):
        if self.position_from_own_start == 0:
            self.is_protected = True
        else:
            pass

    def _set_position_from_own_start_after_jack(self, board_size):
        relative_move = self.position_at_start_of_turn - self.position
        self.position_from_own_start = self.position_from_own_start - relative_move
        # Following line is necessary to properly set your opponents pawn position_from_own_start. If the pawn moves
        # over its own start (and thus above board size), the position needs to be reset.
        self.position_from_own_start = (self.position_from_own_start + board_size) % board_size

    def _update_pawn_positions_by_move_value(self, move_value, board_size):
        self.position_at_start_of_turn = self.position
        self.position += move_value
        self._check_for_finish(board_size)
        self._check_for_negative_position(board_size)
        self._check_for_protection_from_own_0()

    def move_by_card(self, card, game_info, jack_other_pawn_position=None, move_from_7=None):
        if card.rank == 'A':
            if self.home:
                self.home_at_start_of_turn = self.home
                self.home = False
                self.position_at_start_of_turn = self.position
                self.position = 0
                self._check_for_finish(game_info.board_size)
                self._check_for_negative_position(game_info.board_size)
                self._check_for_protection_from_own_0()
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
            self._set_position_from_own_start_after_jack(game_info.board_size)
            self._check_for_finish(game_info.board_size)
            self._check_for_negative_position(game_info.board_size)
            self._check_for_protection_from_own_0()
        elif card.rank == 'K':
            if self.home:
                self.home_at_start_of_turn = self.home
                self.home = False
                self.position_at_start_of_turn = self.position
                self.position = 0
                self._check_for_finish(game_info.board_size)
                self._check_for_negative_position(game_info.board_size)
                self._check_for_protection_from_own_0()
            else:
                # This play would change nothing and is hence undetectable by is_card_play_legal. To detect the illegal
                # play, we set to None
                self.home_at_start_of_turn = None
        else:
            self._update_pawn_positions_by_move_value(card.move_value, game_info.board_size)

    def set_position_relative_to_current_player(self, current_player, game_info):
        if self.color != current_player.color:
            pawn_turn_relative_to_player = (
                    (game_info.player_colors_in_start_order.index(self.color) -
                     game_info.player_colors_in_start_order.index(current_player.color)) %
                    len(game_info.player_colors_in_start_order))
            self.position = (self.position_from_own_start + 16 * pawn_turn_relative_to_player) % game_info.board_size
            self.position_at_start_of_turn = self.position
        else:
            self.position = self.position_from_own_start
            self.position_at_start_of_turn = self.position
