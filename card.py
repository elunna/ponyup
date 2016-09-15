# Use tuples instead of lists
SUITS = ('c', 'd', 'h', 's')
SUITVALUES = {'c': 1, 'd': 2, 'h': 3, 's': 4}
COLORS = {'c': 'green', 'd': 'blue', 'h': 'red', 's': 'white'}

# Fancy way of creating the card/value dictionary.
FACECARDS = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'Z': 15}
RANKS = dict({str(x): x for x in range(2, 10)}, **FACECARDS)

HIDDEN = 'Xx'


class Card:
    def __init__(self, rank, suit):
        if rank not in RANKS:
            raise ValueError('Corrupt card construction - {} is not a valid rank!'.format(rank))
        if suit.lower() not in SUITS:
            raise ValueError('Corrupt card construction - {} is not a valid suit!'.format(suit))

        self.rank = rank
        self.suit = suit.lower()
        self.hidden = True  # Hide cards by default

    def __str__(self):
        """
        Returns the colored string representation
        """
        if self.hidden:
            return HIDDEN
        else:
            return self.rank + self.suit

    def __repr__(self):
        """
        Returns the string representation as Rank/Suit.
        """
        return str(self)

    def __eq__(self, other):
        """
        Returns True if this card is equal to the other card, False otherwise.
        """
        return self.rank == other.rank and self.suit == other.suit

    def __gt__(self, other):
        """
        Returns True if this card's rank is greater than the other card, False otherwise.
        """
        return RANKS[self.rank] > RANKS[other.rank]

    def __lt__(self, other):
        """
        Returns True if this card's rank is lesser than the other card, False otherwise.
        """
        return RANKS[self.rank] < RANKS[other.rank]

    def __hash__(self):
        return hash(str(self))

    def val(self):
        """
        Returns the value of the Cards rank.
        """
        return RANKS[self.rank]

    def peek(self):
        """
        This is how human/hero's are able to view hidden cards.
        """
        return self.rank + self.suit
