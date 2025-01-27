
class Player:
    def __init__(self, color: str):
        self.color = color
        self.pawns = []
        self.hand = []
        # card_history should be reset everytime the deck is dealt
        self.card_history = ''
