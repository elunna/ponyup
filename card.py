#!/usr/bin/env python

# Use tuples instead of lists
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
SUITS = ('c', 'd', 'h', 's')
#  SUITS = ('Clubs', 'Diamonds', 'Hearts', 'Spades')

cardvalues = {
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
            #  exit()
        if suit.lower() not in SUITS:
            raise ValueError('Corrupt card construction - {} is not a valid suit!'.format(suit))
            #  exit()

        self.rank = rank
        self.suit = suit.lower()

    def val(self):
        return cardvalues[self.rank]

    def __str__(self):
        return self.rank + self.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __gt__(self, other):
        return cardvalues[self.rank] > cardvalues[other.rank]

    def __lt__(self, other):
        return cardvalues[self.rank] < cardvalues[other.rank]


if __name__ == "__main__":
    print('Test card construction')
    c1 = Card('A', 's')
    print(c1)
    c2 = Card('2', 's')
    print(c2)

    print('Uppercase suit')
    c3 = Card('3', 'S')
    print(c3)

    # Invalid rank
    try:
        c3 = Card('0', 'd')
    except ValueError as v:
        print(v.args)

    # Invalid suit
    try:
        c5 = Card('5', 'z')
    except ValueError as v:
        print(v.args)

    print
    print('Test equality operators')
    print('{} > {}: {}'.format(c1, c2, c1 > c2))
    print('{} < {}: {}'.format(c1, c2, c1 < c2))
    print('{} = {}: {}'.format(c1, c1, c1 == c1))
    print('{} = {}: {}'.format(c1, c2, c1 == c2))
    print


