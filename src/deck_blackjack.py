from . import deck
from . import playingcard as pc


def mk_blackjack_deck(shoes):
    if shoes < 1:
        raise ValueError('BlackjackDeck must be passed a value of 1 or more for shoes!')
    return pc.std_deck() * shoes


class BlackjackDeck(deck.Deck):
    """ Creates a blackjack deck with the specified number of 'shoes' included.
        4 shoes is the most common size for a Las Vegas blackjack deck.
    """
    def __init__(self, shoes):
        super(BlackjackDeck, self).__init__()
        self.cards = mk_blackjack_deck(shoes)
