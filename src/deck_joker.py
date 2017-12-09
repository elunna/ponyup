from . import deck
from . import joker


class DeckJoker(deck.Deck):
    """ Creates a deck with one Joker. """
    def __init__(self, jokers=1):
        # super(deck.Deck, self).__init__()
        deck.Deck.__init__(self)

        for _ in range(jokers):
            self.cards.append(joker.Joker())
