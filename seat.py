class Seat():
    def __init__(self, player=None):
        self.player = None
        self.hand = None
        self.chips = 0

    def sitdown(self, player):
        pass

    def standup(self, player):
        pass

    def is_empty(self):
        pass

    def has_hand(self):
        pass

    def has_chips(self):
        pass

    def buy_chips(self, amount):
        pass

    def bet(self, amount):
        pass

    def add_card(self, c):
        pass

    def remove_card(self, c):
        pass

    def fold(self, c):
        pass
