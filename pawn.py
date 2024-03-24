
class Pawn():
    def __init__(self, color, position, position_from_own_start, home, finish, protected):
        self.color = color
        self.position = position
        self.previous_position = position
        self.position_from_own_start = position_from_own_start
        self.home = home
        self.finish = finish
        self.previously_in_finish = False
        self.is_protected = protected

    def move(self, move_value, board_size):
        self.previous_position = self.position
        self.position += move_value
        if self.position >= board_size:
            if self.finish:
                self.previously_in_finish = True
            self.finish = True
        elif self.position < board_size:
            if self.finish:
                self.previously_in_finish = True
            self.finish = False
        elif self.position < 0:
            self.position = (self.position + board_size) % board_size
        else:
            pass

    def play_card_on_pawn(self, card, game_info, jack_other_pawn_position = None, move_from_7 = None):
        if card == 'A':
            if self.home:
                self.home = False
                self.position = 0
            else:
                move_value = 1
                self.move(move_value, game_info.board_size)
        if card == '2':
            move_value = 2
            self.move(move_value, game_info.board_size)
        if card == '3':
            move_value = 3
            self.move(move_value, game_info.board_size)
        if card == '4':
            move_value = -4
            self.move(move_value, game_info.board_size)
        if card == '5':
            move_value = 5
            self.move(move_value, game_info.board_size)
        if card == '6':
            move_value = 6
            self.move(move_value, game_info.board_size)

        if card == '7':
            move_value = move_from_7
            self.move(move_value, game_info.board_size)

        if card == '8':
            move_value = 8
            self.move(move_value, game_info.board_size)
        if card == '9':
            move_value = 9
            self.move(move_value, game_info.board_size)
        if card == 'X':
            move_value = 10
            self.move(move_value, game_info.board_size)

        if card == 'J':
            self.position = jack_other_pawn_position

        if card == 'Q':
            move_value = 12
            self.move(move_value, game_info.board_size)

        if card == 'K':
            if self.home:
                self.home = False
                self.position = 0
            else:
                pass

