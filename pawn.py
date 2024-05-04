
class Pawn():
    def __init__(self, color, position, position_from_own_start, home, finish, protected):
        self.color = color
        self.position = position
        self.position_at_start_of_turn = position
        self.position_from_own_start = position_from_own_start
        self.position_from_own_start_at_start_of_turn = position_from_own_start
        self.home = home
        self.home_at_start_of_turn = home
        self.finish = finish
        self.finish_at_start_of_turn = finish
        self.is_protected = protected

    def reset_start_of_turn_bools_for_next_turn(self):
        self.position_at_start_of_turn = self.position
        self.home_at_start_of_turn = self.home
        self.finish_at_start_of_turn = self.finish

    def move_home(self):
        self.position_at_start_of_turn = self.position
        self.position_from_own_start_at_start_of_turn = self.position_from_own_start
        self.home_at_start_of_turn = self.home
        self.position_from_own_start = 0
        self.position = 0
        self.home = True
        self.finish = False
        self.finish_at_start_of_turn = False
        self.is_protected = False

    def check_for_finish(self, board_size):
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

    def check_for_negative_position(self, board_size):
        if self.position < 0:
            self.position = (self.position + board_size) % board_size
            self.is_protected = False
        else:
            pass

    def check_for_protection_from_own_0(self):
        if self.position_from_own_start == 0:
            self.is_protected = True
        else:
            pass

    def set_position_from_own_start_after_jack(self):
        relative_move = self.position_at_start_of_turn - self.position
        self.position_from_own_start = self.position_from_own_start - relative_move

    # this function does not work. Position after a King is not 0 if pawn.color != player.color.
    # If fixed you could play ace and king cards on pawns of others
    def set_position_after_ace_or_king_or_tackle(self):
        relative_move = self.position_from_own_start_at_start_of_turn - self.position_from_own_start
        self.position = self.position - relative_move

    def move(self, move_value, board_size):
        self.position_at_start_of_turn = self.position
        self.position_from_own_start_at_start_of_turn = self.position_from_own_start
        self.position += move_value
        self.position_from_own_start += move_value
        self.check_for_finish(board_size)
        self.check_for_negative_position(board_size)
        self.check_for_protection_from_own_0()

    def move_by_card(self, card, game_info, jack_other_pawn_position=None, move_from_7=None):
        if card.rank == 'A':
            if self.home:
                self.home_at_start_of_turn = self.home
                self.home = False
                self.position_from_own_start_at_start_of_turn = self.position_from_own_start
                self.position_from_own_start = 0
                self.position_at_start_of_turn = self.position
                self.position = 0
                self.check_for_finish(game_info.board_size)
                self.check_for_negative_position(game_info.board_size)
                self.check_for_protection_from_own_0()
            else:
                move_value = 1
                self.move(move_value, game_info.board_size)
        elif card.is_splittable:
            if move_from_7:
                move_value = move_from_7
            else:
                move_value = card.move_value
            self.move(move_value, game_info.board_size)
        elif card.rank == 'J':
            self.position_at_start_of_turn = self.position
            self.position_from_own_start_at_start_of_turn = self.position_from_own_start
            self.position = jack_other_pawn_position
            self.set_position_from_own_start_after_jack()
            self.check_for_finish(game_info.board_size)
            self.check_for_negative_position(game_info.board_size)
            self.check_for_protection_from_own_0()
        elif card.rank == 'K':
            if self.home:
                self.home_at_start_of_turn = self.home
                self.home = False
                self.position_from_own_start_at_start_of_turn = self.position_from_own_start
                self.position_from_own_start = 0
                self.position_at_start_of_turn = self.position
                self.position = 0
                self.check_for_finish(game_info.board_size)
                self.check_for_negative_position(game_info.board_size)
                self.check_for_protection_from_own_0()
            else:
                # This play would change nothing and is hence indetectable by is_card_play_legal. To detect the illegal
                # play, we set to None
                self.home_at_start_of_turn = None
        else:
            self.move(card.move_value, game_info.board_size)

