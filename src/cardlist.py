""" A CardList is a structure for manipulating PlayingCards.
    PlayingCards have more complexities that this will be able to manage.
"""
import random


class CardList(object):
    def __init__(self, cards=None):
        if cards:
            self.cards = cards
        else:
            self.cards = []

    def __contains__(self, c):
        """ Returns True if the given Card is in the CardList, False otherwise. """
        return c in self.cards

    def __len__(self):
        """ Returns how many cards there are. """
        return len(self.cards)

    def __str__(self):
        """ Returns a list of string representations of all cards in the CardList. """
        return ' '.join([str(c) for c in self.cards])

    def add(self, card):
        """ Adds a card. """
        self.cards.append(card)

    def count_suit(self, suit):
        """ Counts how many cards of the given suit occur in the card list. """
        return sum(1 for c in self.cards if c.suit == suit)

    def count_rank(self, rank):
        """ Counts how many cards of the given rank occur in the card list. """
        return sum(1 for c in self.cards if c.rank == rank)

    def discard(self, card):
        """ Removes a card and returns it. """
        if card not in self.cards:
            raise ValueError('Card {} is not in this CardList!'.format(str(card)))
        i = self.cards.index(card)
        copy = self.cards.pop(i)
        return copy

    def get_upcards(self):
        """ Returns a list of all the face-up cards  """
        return [c for c in self.cards if c.hidden is False]

    def is_empty(self):
        """ Returns True if there are 0 cards, False otherwise. """
        return len(self.cards) == 0

    def peek(self):
        """ Returns a list of strings representing the cards """
        return [c.peek() for c in self.cards]

    def remove(self, c):
        """ Removes the specified Card if it's here, or returns None if it isn't here. """
        if c in self.cards:
            return self.cards.remove(c)
        else:
            return None

    def reveal(self):
        """ Turns all cards faceup. """
        for c in self.cards:
            c.hidden = False

    def shuffle(self, x=1):
        """ Shuffles the CardList once.  """
        for _ in range(x):
            random.shuffle(self.cards)

    def sort(self):
        """ Sorts the cards. """
        self.cards.sort(key=lambda x: x.val())
        # return sorted(self.cards)

    def strip_ranks(self, ranks):
        """ Takes a list of cards, removes the rank(s) given, and returns a list of
            the leftovers.  There can be more than one rank passed.
        """
        return [c for c in self.cards if c.rank not in ranks]

    def strip_suits(self, suits):
        """ Takes a list of cards, removes the suit given, and returns a list of the
            leftovers. There can only be one suit passed.
        """
        return [c for c in self.cards if c.suit not in suits]
