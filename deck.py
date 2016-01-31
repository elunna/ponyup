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

    def display(self):
        for i, c in enumerate(self.cards):
            if i % 13 == 0 and i != 0:
                print()
            # print(c.rank + c.suit)
            #  print(str(c), ' ', end='')
            print('{} '.format(str(c)), end='')
        print()

    def shuffle(self):
        random.shuffle(self.cards)
        # self.cards.shuffle()

    def sort(self):
        #  sorted(self.cards)
        self.cards.sort()

    def deal(self):
        return self.cards.pop()

    def str(self):
        self.display()

    def __len__(self):
        return len(self.cards)


def create_deck():
    # Create and return a full deck of cards Using Card objects
    # Use only the first letter of the suits
    deck = [card.Card(r, s.lower()[0]) for s in SUITS for r in RANKS]
    return deck


if __name__ == '__main__':
    print('New Deck')
    d = Deck()
    d.display()
    print('')
    print('Shuffling the deck')
    d.shuffle()
    d.display()

    print('')
    print('dealing out 10 cards and creating a new deck')

    cards = [d.deal() for c in range(10)]
    d2 = Deck(cards)
    d2.display()

    print('')
    print('Sorting the deck')
    d3 = Deck(d2.sort())
    d3.display()
