#!/usr/bin/env python

# Use tuples instead of lists
SUITS = ('c', 'd', 'h', 's')

RANKS = {
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
        self.hidden = True  # Hide cards by default

    def val(self):
        return RANKS[self.rank]

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
        return RANKS[self.rank] > RANKS[other.rank]

    def __lt__(self, other):
        return RANKS[self.rank] < RANKS[other.rank]
