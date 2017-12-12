""" Evaluates poker hands """

import itertools
from . import cardlist
from . import playingcard as pc
from collections import namedtuple

Ranklist = namedtuple('Ranklist', ['quantity', 'rank'])
HANDSIZE = 5
MULTIPLIERS = (100000000, 1000000, 10000, 100, 1)
FIVEHIGH, ACEHIGH = 5, 14

HANDTYPES = {
    'ROYAL FLUSH':      100000000000,
    'STRAIGHT FLUSH':   90000000000,
    'QUADS':            80000000000,
    'FULL HOUSE':       70000000000,
    'FLUSH':            60000000000,
    'STRAIGHT':         50000000000,
    'TRIPS':            40000000000,
    'TWO PAIR':         30000000000,
    'PAIR':             20000000000,
    'HIGH CARD':        0,
    'INVALID': -1
}

DRAWTYPES = {
    'STRAIGHT FLUSH DRAW': 5000,
    'FLUSH DRAW': 4000,
    'STRAIGHT DRAW': 2000,
    'GUTSHOT DRAW': 1000,
    'BACKDOOR FLUSH DRAW': 200,
    'BACKDOOR STRAIGHT DRAW': 100,
    '2 SUITED DRAW': 20,
    '2 CONNECTED DRAW': 10,
    'HIGH CARD DRAW': 0
}


class PokerHand(cardlist.CardList):
    def __init__(self, cards):
        self.cards = cards

    def value(self):
        return get_value(self.cards)

    def rank(self):
        return get_type(self.value())

    def desc(self):
        return get_description(self.value(), self.cards)


def is_wheel(cards):
    """ Check if the group of cards(passed as a rank dictionary) counts as a 'wheel
        straight, or A2345.
    """
    return set(rank_dict(cards).keys()) == {'A', '2', '3', '4', '5'}


def dominant_suit(cards):
    """ Finds which suit occurs with the greatest frequency in a list of Cards.
        If there are an equal # of suits between cards, count the higher ranked
        cards.  If a tie is further needed to be broken because the suited cards
        are the same rank, break the tie by using the traditional ranking of suits.
    """
    suitdict = suitedcard_dict(cards)
    domcount = max(len(s) for s in suitdict.values())

    # Count how many ties there are.
    tied = [s for s in suitdict if len(suitdict[s]) == domcount]

    if len(tied) == 1:
        return tied.pop()
    else:
        # We have to find the more dominant suit by comparing ranks
        highscore = 0
        highsuit = None

        for s in tied:
            score = score_cardlist(suitdict[s])
            if score > highscore:
                highscore = score
                highsuit = s
        return highsuit


def is_set(cards):
    """ Return True if all cards all unique, False otherwise.
    """
    return len(set(cards)) == len(cards)


def is_straight(cards):
    """ Check the list of cards to see if it is a valid straight. If it is,
        returns the highest rank in straight, otherwise returns -1.
    """
    if not is_validhand(cards):
        return 0
    elif get_allgaps(cards) == 0:
        return max(cards).val()

    for c, r in zip(sorted(cards), [2, 3, 4, 5, 14]):
        if c.val() != r:
            return 0
    return 5


def is_suited(cards):
    """ Returns True if all the cards in the list match the same suit. """
    return len(suitedcard_dict(cards)) == 1


def is_validhand(cards):
    """ Returns True if the cardlist is 5 unique cards. """
    return len(set(cards)) == 5


def find_best_hand(cards):
    """ Takes a list of cards and determines the best available 5 card hand and
        returns that hand as a Hand.
    """
    if len(cards) < HANDSIZE:
        return None
    combos = [c for c in itertools.combinations(cards, HANDSIZE)]

    bestcombo, bestvalue = None, 0

    for c in combos:
        val = get_value(c)
        if val > bestvalue:
            bestcombo, bestvalue = c, val
    return bestcombo


def get_allgaps(cards):
    """ Takes a list of cards and determines how many gaps are between all the
        ranks (when they occur in sorted order. Should work regardless of order.)
    """
    ordered = sorted(cards)
    gaps = 0

    for i, c in enumerate(ordered):
        if i == len(cards) - 1:
            break
        g = get_gap(c, ordered[i + 1])
        if g == -1:
            raise ValueError('Pair detected while attempting to parse connected cards!')
        gaps += g
    return gaps


def get_gap(card1, card2):
    """ Return how many spaces are between the ranks of 2 cards.
        Example: For 87, 8 - 7 = 1, but the gap is actually 0. Paired cards have no gap.
    """
    if card1.rank == card2.rank:
        return -1

    return abs(card1.val() - card2.val()) - 1


def get_description(value, cards):
    """ Returns a text description of the passed pokerhand. """
    ranks = rank_list(cards)
    RANK = get_type(value)
    BASEVALUE = 10000000000

    if len(cards) == 0:
        return 'No cards!'
    elif RANK in ['STRAIGHT', 'STRAIGHT FLUSH']:
        if value % BASEVALUE == 0:
            return '5 High'
        else:
            return '{} High'.format(ranks[0].rank)
    elif RANK in ['QUADS', 'TRIPS', 'PAIR']:
        return '{}\'s'.format(ranks[0].rank)
    elif RANK == 'FULL HOUSE':
        return '{}\'s full of {}\'s'.format(
            ranks[0].rank, ranks[1].rank)
    elif RANK == 'TWO PAIR':
        return '{}\'s and {}\'s'.format(
            ranks[0].rank, ranks[1].rank)
    else:
        return '{} High'.format(ranks[0].rank)


def get_type(value):
    """ Determine the type of hand given the numerical value. """
    if value < 0:
        return 'INVALID'
    else:
        roundedval = round(value, -10)

    for v in HANDTYPES:
        if HANDTYPES[v] == roundedval:
            return v
    raise ValueError('Type error: Cannot find type!')


def get_value(cards):
    """ Takes a list of cards, calculates the highest hand rank it qualifies for
        and returns its integer value. If a hand is less than 5 cards, we can
        still calculate what type of hand it is("pair", "two pair", etc), but
        having less than 5 cards automatically filters out the hands that require
        5: straights, flushes, full house, etc.
    """
    ranklist = rank_list(sorted(cards))

    if len(ranklist) < 5:
        return score_pair_hands(cards)
    elif len(ranklist) == HANDSIZE:
        # Returns the value of a non-pair hand.

        straight_chk = is_straight(cards)
        if is_suited(cards):
            if straight_chk == ACEHIGH:
                return HANDTYPES['ROYAL FLUSH']
            elif straight_chk == FIVEHIGH:
                return HANDTYPES['STRAIGHT FLUSH']
            elif straight_chk > FIVEHIGH:
                return HANDTYPES['STRAIGHT FLUSH'] + straight_chk * MULTIPLIERS[0]
            else:
                return HANDTYPES['FLUSH'] + score_ranklist(ranklist)
        elif straight_chk == FIVEHIGH:
            return HANDTYPES['STRAIGHT']
        elif straight_chk:
            return HANDTYPES['STRAIGHT'] + score_ranklist(ranklist)
        else:
            return HANDTYPES['HIGH CARD'] + score_ranklist(ranklist)
    else:
        return HANDTYPES['INVALID']


def rank_dict(cards):
    """ Returns a dictionary of rank/counts for the list of cards. """
    ranks = {}
    for c in cards:
        ranks[c.rank] = ranks.get(c.rank, 0) + 1
    return ranks


def rank_list(cards):
    """ Returns a list of quantity/rank pairs by making a rank dictionary,
        converting it to a list and sorting it by rank.
    """
    ranks = rank_dict(cards)
    L = [Ranklist(quantity=ranks[r], rank=r) for r in ranks]
    return sorted(L, key=lambda x: (-x.quantity, -pc.RANKS[x.rank]))


def remove_pairs(cards):
    """ Goes through a list of cards and removes any extra pairs. """
    cards = sorted(cards)
    newlist = []
    for i, c in enumerate(sorted(cards)):
        if i == 0:
            newlist.append(c)
        elif c.rank != cards[i - 1].rank:
            newlist.append(c)
    return newlist


def suitedcard_dict(cards):
    """ Returns a dictionary of suits and card lists. Useful for dividing a list
        of cards into all the separate suits.
    """
    suits = {}
    for c in cards:
        suits.setdefault(c.suit, []).append(c)  # Dict grouping
    return suits


def score_cardlist(cards):
    """ Calculates and returns the score of a sorted list of 5 cards.
        Precondition:  Hand should be ordered by highest value first, lowest last
    """
    score = 0
    for i, c in enumerate(sorted(cards)):
        if i > 0:
            multiplier = 10 ** (i * 2)
        else:
            multiplier = 1
        score += pc.RANKS[c.rank] * multiplier
    return score


def score_pair_hands(cards):
    """ Calculates the value of a hand that fits into the 'pair type' category:
        pairs, two-pairs, sets, full-houses, and quads.
    """
    ranklist = rank_list(sorted(cards))

    # Returns the value of a pair-type hand.
    if len(ranklist) > 1:
        if ranklist[0].quantity == 3 and ranklist[1].quantity == 2:
            return HANDTYPES['FULL HOUSE'] + score_ranklist(ranklist)
        elif ranklist[0].quantity == 2 and ranklist[1].quantity == 2:
            return HANDTYPES['TWO PAIR'] + score_ranklist(ranklist)

    if ranklist[0].quantity == 1:
        return HANDTYPES['HIGH CARD'] + score_ranklist(ranklist)
    elif ranklist[0].quantity == 2:
        return HANDTYPES['PAIR'] + score_ranklist(ranklist)
    elif ranklist[0].quantity == 3:
        return HANDTYPES['TRIPS'] + score_ranklist(ranklist)
    elif ranklist[0].quantity == 4:
        return HANDTYPES['QUADS'] + score_ranklist(ranklist)


def score_ranklist(ranklist):
    """ Calculates and returns the score of a sorted list of 5 cards.
        Precondition: Hand should be ordered by highest value first, lowest last
    """
    score = 0
    for i, c in enumerate(ranklist):
        score += pc.RANKS[c[1]] * MULTIPLIERS[i]
    return score
