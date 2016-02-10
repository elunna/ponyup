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
    def __init__(self, cards=None):
        if cards is None:
            self.cards = create_deck()
        else:
            self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        #  self.cards.sort()
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
                print()
            #  print('{} '.format(str(c)), end='')
            _str += '{} '.format(str(c))
        return _str

    def __len__(self):
        return len(self.cards)


def create_deck():
    # Create and return a full deck of cards Using Card objects
    # Use only the first letter of the suits
    deck = [card.Card(r, s.lower()[0]) for s in SUITS for r in RANKS]
    return deck


if __name__ == '__main__':
    print('New Deck')
    d1 = Deck()
    print(d1)
    print('')
    print('Shuffling the deck')
    d1.shuffle()
    print(d1)

    print('')
    print('dealing out 10 cards and creating a new deck')

    cards = [d1.deal() for c in range(10)]
    d2 = Deck(cards)
    print(d2)

    d1 = Deck()
    d1.shuffle()
    print('')
    print('Sorting the deck')
    d1.sort()

    print(d1)
