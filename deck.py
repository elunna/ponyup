#!/usr/bin/env python
'''
Creates a Deck of cards.
'''
from __future__ import print_function
import card
import random


class Deck():
    def __init__(self, cards=None):
        if cards is None:
            self.cards = standard_deck()
        else:
            self.cards = cards
        # Give it a good shuffle.
        for i in range(10):
            self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort(key=lambda x: x.val())

    def deal(self):
        return self.cards.pop()

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            return None

    def contains(self, card):
        return card in self.cards

    def __str__(self):
        _str = ''
        for i, c in enumerate(self.cards):
            if i % 13 == 0 and i != 0:
                _str += '\n'
            _str += '{} '.format(str(c))
        return _str

    def __len__(self):
        return len(self.cards)


class Deck1Joker(Deck):
    def __init__(self):
        self.cards = standard_deck()
        joker = card.Card('Z', 's')
        self.cards.append(joker)


class Deck2Joker(Deck):
    def __init__(self):
        self.cards = standard_deck()
        joker1 = card.Card('Z', 's')
        joker2 = card.Card('Z', 'c')
        self.cards.append(joker1)
        self.cards.append(joker2)


def standard_deck():
    # Leave out Jokers
    return [card.Card(r, s[0])
            for s in card.SUITS for r in card.RANKS if r != 'Z']
