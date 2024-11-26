class Card():
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
        self.is_splittable = False
        if rank == 'A':
            self.move_value = 1
        if rank == '2':
            self.move_value = 2
        if rank == '3':
            self.move_value = 3
        if rank == '4':
            self.move_value = -4
        if rank == '5':
            self.move_value = 5
        if rank == '6':
            self.move_value = 6

        if rank == '7':
            self.move_value = 7
            self.is_splittable = True

        if rank == '8':
            self.move_value = 8
        if rank == '9':
            self.move_value = 9
        if rank == 'X':
            self.move_value = 10

        if rank == 'J':
            self.move_value = 0

        if rank == 'Q':
            self.move_value = 12

        if rank == 'K':
            self.move_value = 0

