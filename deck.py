#!/usr/bin/env python
"""
Creates a Deck of cards.
"""
from __future__ import print_function
import card
import random


class Deck():
    """
    Creates a standard 52 card deck, with no Jokers.
    """
    def __init__(self, cards=None):
        if cards is None:
            self.cards = \
                [card.Card(r, s[0]) for s in card.SUITS for r in card.RANKS if r != 'Z']
        else:
            self.cards = cards

    def __str__(self):
        """
        Returns a string showing all the cards in the deck.
        """
        _str = ''
        for i, c in enumerate(self.cards):
            if i % 13 == 0 and i != 0:
                _str += '\n'
            _str += '{} '.format(str(c))
        return _str.strip()

    def __len__(self):
        """
        Returns how many cards are in the Deck.
        """
        return len(self.cards)

    def __contains__(self, card):
        """
        Returns True if the given Card is in the deck, False otherwise.
        """
        return card in self.cards

    def shuffle(self, x):
        """
        Shuffles the deck of cards once.
        """
        for i in range(x):
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

    def is_empty(self):
        """
        Returns True if the Deck is empty, False otherwise.
        """
        return len(self.cards) == 0

    def remove(self, card):
        """
        Removes the specified Card from the deck.
        """
        if card in self.cards:
            self.cards.remove(card)
        else:
            return None

    def remove_cards(self, cards):
        """
        Removes a sequence of cards from the deck. If a card in the sequence is not in the deck
        it is simply ignored.
        """
        for c in cards:
            self.remove(c)

    def unhide(self):
        """
        Goes through all cards in the deck and unhides them.
        """
        for c in self.cards:
            c.hidden = False
