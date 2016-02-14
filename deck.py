#!/usr/bin/env python
'''
Creates a Deck of cards.
'''
from __future__ import print_function
from card import SUITS
from card import RANKS
import card
import random


class Deck():
    def __init__(self, cards=None, hidden=True):
        if cards is None:
            self.cards = [card.Card(r, s.lower()[0]) for s in SUITS for r in RANKS]
        else:
            self.cards = cards

        if hidden is False:
            for c in self.cards:
                c.hidden = False

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort(key=lambda x: x.val())

    def deal(self):
        return self.cards.pop()

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def __str__(self):
        _str = ''
        for i, c in enumerate(self.cards):
            if i % 13 == 0 and i != 0:
                _str += '\n'
            _str += '{} '.format(str(c))
        return _str

    def __len__(self):
        return len(self.cards)


if __name__ == '__main__':
    print('New hidden Deck')
    hiddendeck = Deck()
    print(hiddendeck)

    print('New non-hidden Deck')
    showcards = Deck(hidden=False)
    print(showcards)

    print('Shuffling the deck')
    showcards.shuffle()
    print(showcards)

    print('')
    print('dealing out 10 cards and creating a new deck')

    cards = [showcards.deal() for c in range(10)]
    anotherdeck = Deck(cards)
    print(anotherdeck)

    showcards = Deck(hidden=False)
    showcards.shuffle()
    print('')
    print('Sorting the deck')
    showcards.sort()

    print(showcards)
