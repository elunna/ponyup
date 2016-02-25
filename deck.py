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

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort(key=lambda x: x.val())

    def deal(self):
        return self.cards.pop()

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)

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


def standard_deck():
    # Leave out Jokers
    return [card.Card(r, s[0])
            for s in card.SUITS for r in card.RANKS if r != 'Z']


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
