"""
  " Creation and management of a Deck of cards.
  """
from . import playingcard as pc


class Deck(object):
    """ Manages a deck of Cards. The deck is created using that list,
        Otherwise, we create the deck as a standard 52 card deck of PlayingCards.
    """

    def __init__(self, cards=None):
        if cards is None:
            self.cards = pc.std_deck()
        else:
            self.cards = cards

    def __len__(self):
        """ Returns how many cards are in the CardList. """
        return len(self.cards)

    def deal(self):
        """ Removes the top card off the deck and returns it. Raises an exception
            if the deck is empty.
        """
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            raise Exception('Deck is empty, cannot deal cards!')
