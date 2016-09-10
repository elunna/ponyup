import deck
import card


class Deck2Joker(deck.Deck):
    """
    Creates a deck with two Jokers.
    """
    def __init__(self):
        super().__init__()
        self.cards.append(card.JOKER1)
        self.cards.append(card.JOKER2)
