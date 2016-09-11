import deck
import joker


class Deck1Joker(deck.Deck):
    """
    Creates a deck with one Joker.
    """
    def __init__(self):
        super().__init__()
        self.cards.append(joker.JOKER1)
