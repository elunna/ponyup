#!/usr/bin/env python
"""
Creates a Deck of cards.
"""
from __future__ import print_function
import card
import random


class Deck():
    def __init__(self, cards=None):
        if cards is None:
            self.cards = make_deck()
        else:
            self.cards = cards
        # Give it a good shuffle.
        for i in range(10):
            self.shuffle()

    def shuffle(self):
        """
        Shuffles the deck of cards once.
        """
        random.shuffle(self.cards)

    def sort(self):
        """
        Sorts the deck by card rank.
        """
        self.cards.sort(key=lambda x: x.val())

    def deal(self):
        """
        Removes the top card off the deck and returns it. Raises an exception if the deck is
        empty.
        """
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            raise Exception('Deck is empty, cannot deal cards!')

    def remove(self, card):
        """
        Removes the specified Card from the deck.
        """
        if card in self.cards:
            self.cards.remove(card)
        else:
            return None

    def contains(self, card):
        """
        Returns True if the given Card is in the deck, False otherwise.
        """
        return card in self.cards

    def is_empty(self):
        """
        Returns True if the Deck is empty, False otherwise.
        """
        return len(self.cards) == 0

    def __str__(self):
        """
        Returns a string showing all the cards in the deck.
        """
        _str = ''
        for i, c in enumerate(self.cards):
            if i % 13 == 0 and i != 0:
                _str += '\n'
            _str += '{} '.format(str(c))
        return _str

    def __len__(self):
        """
        Returns how many cards are in the Deck.
        """
        return len(self.cards)

    def unhide(self):
        """
        Goes through all cards in the deck and unhides them.
        """
        for c in self.cards:
            c.hidden = False


class Deck1Joker(Deck):
    """
    Creates a deck with one Joker.
    """
    def __init__(self):
        self.cards = make_deck()
        joker = card.Card('Z', 's')
        self.cards.append(joker)


class Deck2Joker(Deck):
    """
    Creates a deck with two Jokers.
    """
    def __init__(self):
        self.cards = make_deck()
        joker1 = card.Card('Z', 's')
        joker2 = card.Card('Z', 'c')
        self.cards.append(joker1)
        self.cards.append(joker2)


def make_deck():
    """
    Returns a standard 52 card deck, with no Jokers.
    """
    return [card.Card(r, s[0])
            for s in card.SUITS for r in card.RANKS if r != 'Z']
