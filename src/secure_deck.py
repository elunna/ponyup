from . import deck


class SecureDeck(object):
    """ Manages a deck of Cards using a stack structure.
        If cards is a list of Cards, the deck is created using that list,
        Otherwise, we create the deck as a standard 52 card deck of PlayingCards.
    """

    def __init__(self):
        self.cards = deck.std_deck()
