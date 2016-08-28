import colors

# Use tuples instead of lists
SUITS = ('c', 'd', 'h', 's')

# Fancy way of creating the card/value dictionary.
FACECARDS = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'Z': 15}
RANKS = dict({str(x): x for x in range(2, 10)}, **FACECARDS)

COLORS = {'c': 'green', 'd': 'blue', 'h': 'red', 's': 'white'}


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
            return colors.color('Xx', 'gray')

        return colors.color(self.rank + self.suit, COLORS[self.suit])

    def __repr__(self):
        return self.rank + self.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __gt__(self, other):
        return RANKS[self.rank] > RANKS[other.rank]

    def __lt__(self, other):
        return RANKS[self.rank] < RANKS[other.rank]

    def __hash__(self):
        return hash(str(self))
