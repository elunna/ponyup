""" A CardList is a structure for manipulating PlayingCards.
    PlayingCards have more complexities that this will be able to manage.
"""
import random


class CardList(object):
    def __init__(self, cards=[]):
        self.cards = cards

    def __len__(self):
        """ Returns how many cards are in the CardList. """
        return len(self.cards)

    def __str__(self):
        """ Returns a list of string representations of all cards in the CardList. """
        return ' '.join([str(c) for c in self.cards])

    def __contains__(self, c):
        """ Returns True if the given Card is in the CardList, False otherwise. """
        return c in self.cards

    def shuffle(self, x=1):
        """ Shuffles the CardList once.  """
        for _ in range(x):
            random.shuffle(self.cards)

    def is_empty(self):
        """ Returns True if the CardList is empty, False otherwise. """
        return len(self.cards) == 0

    def remove(self, c):
        """ Removes the specified Card from the CardList. """
        if c in self.cards:
            self.cards.remove(c)
        else:
            return None

    def sort(self):
        """ Sorts the deck by card rank.  """
        # self.cards.sort(key=lambda x: x.val())
        self.cards.sort()

    def toggle_hidden(self, hidden):
        """ Goes through all cards in the CardList and set them to the designated hidden status."""
        for c in self.cards:
            c.hidden = hidden
