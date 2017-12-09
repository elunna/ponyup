from . import deck
from . import playingcard as pc


class PiquetDeck(deck.Deck):
    """ Creates a 48 card Pinochle deck with 2 of each rank: 9, T, J, Q, K, A. """
    def __init__(self):
        super(PiquetDeck, self).__init__()
        pinochle_cards = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.cards = [pc.PlayingCard(r, s[0]) for s in pc.SUITS
                      for r in pc.RANKS if r in pinochle_cards]
