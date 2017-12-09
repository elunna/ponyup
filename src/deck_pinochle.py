from . import deck
from . import playingcard as pc


class PinochleDeck(deck.Deck):
    """ Creates a 48 card Pinochle deck with 2 of each rank: 9, T, J, Q, K, A. """
    def __init__(self):
        super(PinochleDeck, self).__init__()
        pinochle_cards = ['9', 'T', 'J', 'Q', 'K', 'A']
        c = [pc.PlayingCard(r, s[0]) for s in pc.SUITS for r in pc.RANKS if r in pinochle_cards]

        self.cards = c + c
