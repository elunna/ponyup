from . import deck
from . import playingcard


def mk_joker_deck(jokers):
    cards = playingcard.std_deck()
    for _ in range(jokers):
        cards.append(playingcard.Joker())
    return cards


class DeckJoker(deck.Deck):
    """ Creates a deck with one Joker. """
    def __init__(self, jokers):
        deck.Deck.__init__(self)
