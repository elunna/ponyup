from . import deck_secure as ds
from . import playingcard


def mk_joker_deck(jokers):
    cards = playingcard.std_deck()
    for _ in range(jokers):
        cards.append(playingcard.Joker())
    return cards


class DeckJoker(ds.SecureDeck):
    """ Creates a deck with one Joker. """
    def __init__(self, jokers):
        ds.SecureDeck.__init__(self)
