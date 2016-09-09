import deck
import card


class Deck2Joker(deck.Deck):
    """
    Creates a deck with two Jokers.
    """
    def __init__(self):
        super().__init__()
        joker1 = card.Card('Z', 's')
        joker2 = card.Card('Z', 'c')
        self.cards.append(joker1)
        self.cards.append(joker2)
