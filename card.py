#!/usr/bin/env python

# Use tuples instead of lists
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
SUITS = ('c', 'd', 'h', 's')

VALUES = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}


class Card:
    def __init__(self, rank, suit):
        if rank not in RANKS:
            raise ValueError('Corrupt card construction - {} is not a valid rank!'.format(rank))
        if suit.lower() not in SUITS:
            raise ValueError('Corrupt card construction - {} is not a valid suit!'.format(suit))

        self.rank = rank
        self.suit = suit.lower()

        # Hide cards by default?
        # Probably works better that way since they originate from decks first.
        self.hidden = True

    def val(self):
        return VALUES[self.rank]

    def __str__(self):
        if self.hidden:
            return 'Xx'
        else:
            return self.rank + self.suit

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __gt__(self, other):
        return VALUES[self.rank] > VALUES[other.rank]

    def __lt__(self, other):
        return VALUES[self.rank] < VALUES[other.rank]
