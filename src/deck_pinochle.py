from . import deck
from . import playingcard as pc

""" A Pinochle deck is usually 48 cards(a double 24 deck),
    but it can also be an 80 card deck (quadruple 20 card deck.)
    A pinochle deck consists of two copies of each of 9, 10, J, Q, K, and A cards of all four suits.
    Aces are always considered high.
    Pinochle follows a nonstandard card ordering.
    The complete ordering from highest to lowest is A, 10, K, Q, J, 9.
"""


def mk_pinochle_deck():
    pinochle_cards = ['9', 'T', 'J', 'Q', 'K', 'A']
    c = [pc.PlayingCard(r, s[0]) for s in pc.SUITS for r in pc.RANKS if r in pinochle_cards]

    return c + c


class PinochleDeck(deck.Deck):
    """ Creates a 48 card Pinochle deck with 2 of each rank: 9, T, J, Q, K, A. """
    def __init__(self):
        super(PinochleDeck, self).__init__()
        self.cards = mk_pinochle_deck()
