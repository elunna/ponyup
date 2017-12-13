""" Manages a regular hand of cards. """

from . import evaluator as ev


class Hand():
    """ Hand object: Pretty flexible structure for letting players manage general Cards.
    """
    def __init__(self):
        self.cards = []

    def __len__(self):
        """ Returns how many cards there are. """
        return len(self.cards)

    def __str__(self):
        """ Returns a list of string representations of all cards in the CardList. """
        return ' '.join([str(c) for c in self.cards])

    def add(self, card):
        """ Adds a card. """
        self.cards.append(card)

    def discard(self, card):
        """ Removes a card and returns it. """
        if card not in self.cards:
            raise ValueError('Card {} is not in this!'.format(str(card)))
        i = self.cards.index(card)
        copy = self.cards.pop(i)
        return copy

    def get_upcards(self):
        """ Returns a list of all the face-up cards  """
        return [c for c in self.cards if c.hidden is False]

    def is_empty(self):
        """ Returns True if there are 0 cards, False otherwise. """
        return len(self.cards) == 0

    def reveal(self):
        """ Turns all cards faceup. """
        for c in self.cards:
            c.hidden = False


class PokerHand(Hand):
    """ PokerHand object: This is more specialized for Poker variations.
        * This hand will keep track of the value of a hand as it is updated.
        * The cards will not be accessible by the outside, only by adding or
        * discarding from the CardList methods.
    """
    def __init__(self):
        # Initialize as a new empty Hand
        Hand.__init__(self)
        self.update()

    def update(self):
        self.value = ev.ev.get_value(self.cards)
        self.description = ev.get_description(self.value, self.cards)
        self.rank = ev.get_type(self.value)
