import deck
import card


class Deck1Joker(deck.Deck):
    """
    Creates a deck with one Joker.
    """
    def __init__(self):
        super().__init__()
        self.cards.append(card.JOKER1)
