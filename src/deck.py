"""
  " Creation and management of a Deck of cards.
  """
import random
from . import playingcard as pc
from . import joker


def std_deck():
    return [pc.PlayingCard(r, s) for s in pc.SUITS
            for r in pc.RANKS if r != joker.joker_rank]


class Deck(object):
    """ Manages a deck of Cards using a stack structure.
        If cards is a list of Cards, the deck is created using that list,
        Otherwise, we create the deck as a standard 52 card deck of PlayingCards.
    """

    def __init__(self, cards=None):
        if cards is None:
            self.cards = std_deck()
        else:
            self.cards = cards

    def __str__(self):
        """ Returns a string showing all the cards in the deck. """
        _str = ''
        for i, c in enumerate(self.cards):
            if i % 13 == 0 and i != 0:
                _str += '\n'
            _str += '{} '.format(str(c))
        return _str.strip()

    def __len__(self):
        """ Returns how many cards are in the Deck.  """
        return len(self.cards)

    def __contains__(self, c):
        """ Returns True if the given Card is in the deck, False otherwise.  """
        return c in self.cards

    def shuffle(self, x=1):
        """ Shuffles the deck of cards once.  """
        for _ in range(x):
            random.shuffle(self.cards)

    def sort(self):
        """ Sorts the deck by card rank.  """
        self.cards.sort(key=lambda x: x.val())

    def deal(self):
        """ Removes the top card off the deck and returns it. Raises an exception
            if the deck is empty.
        """
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            raise Exception('Deck is empty, cannot deal cards!')

    def is_empty(self):
        """ Returns True if the Deck is empty, False otherwise. """
        return len(self.cards) == 0

    def remove(self, c):
        """ Removes the specified Card from the deck. """
        if c in self.cards:
            self.cards.remove(c)
        else:
            return None

    def remove_cards(self, cards):
        """ Removes a sequence of cards from the deck. If a card in the sequence
            is not in the deck it is simply ignored.
        """
        for c in cards:
            self.remove(c)

    def unhide(self):
        """ Goes through all cards in the deck and unhides them.  """
        for c in self.cards:
            c.hidden = False
