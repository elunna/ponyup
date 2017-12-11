""" A CardList is a structure for manipulating PlayingCards.
    PlayingCards have more complexities that this will be able to manage.
"""
import random
from collections import namedtuple
from . import playingcard as pc

Ranklist = namedtuple('Ranklist', ['quantity', 'rank'])


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

    def is_set(self):
        """ Return False if items contains any duplicate entries and True if they
            are all unique.
        """
        return len(set(self.cards)) == len(self.cards)

    def rank_dict(self):
        """ Returns a dictionary of rank/counts for the list of cards. """
        ranks = {}
        for c in self.cards:
            ranks[c.rank] = ranks.get(c.rank, 0) + 1
        return ranks

    def rank_list(self):
        """ Returns a list of quantity/rank pairs by making a rank dictionary,
            converting it to a list and sorting it by rank.
        """
        ranks = self.rank_dict()
        L = [Ranklist(quantity=ranks[r], rank=r) for r in ranks]
        return sorted(L, key=lambda x: (-x.quantity, -pc.RANKS[x.rank]))

    def suit_dict(self):
        """ Returns a dictionary of quantity/suit pair counts. """
        suits = {}
        for c in self.cards:
            suits[c.suit] = suits.get(c.suit, 0) + 1
        return suits

    def count_suit(self, suit):
        """ Counts how many cards of the given suit occur in the card list. """
        return sum(1 for c in self.cards if c.suit == suit)

    def count_rank(self, rank):
        """ Counts how many cards of the given rank occur in the card list. """
        return sum(1 for c in self.cards if c.rank == rank)

    def suitedcard_dict(self):
        """ Returns a dictionary of suits and card lists. Useful for dividing a list
            of cards into all the separate suits.
        """
        suits = {}
        for c in self.cards:
            key = c.suit
            suits.setdefault(key, []).append(c)  # Dict grouping
        return suits

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

    def remove_pairs(self):
        """ Goes through a list of cards and removes any extra pairs. """
        cards = sorted(self.cards)
        newlist = []
        for i, c in enumerate(sorted(cards)):
            if i == 0:
                newlist.append(c)
            elif c.rank != cards[i - 1].rank:
                newlist.append(c)
        return newlist

    def is_suited(self):
        """ Returns True if all the cards in the list match the same suit. """
        suit = self.cards[0].suit
        for c in self.cards:
            if c.suit != suit:
                return False
        return True
