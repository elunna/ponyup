import deck
import joker


class Deck2Joker(deck.Deck):
    """
    Creates a deck with two Jokers.
    """
    def __init__(self):
        super().__init__()
        self.cards.append(joker.JOKER1)
        self.cards.append(joker.JOKER2)
