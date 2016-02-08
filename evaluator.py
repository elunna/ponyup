#!/usr/bin/env python
""" Evaluates poker hands """

from __future__ import print_function
import card
import hand
import itertools
#  import operator

MULTIPLIERS = (100000000, 1000000, 10000, 100, 1)

HANDTYPES = {
    'ROYAL FLUSH':      100000000000,
    'STRAIGHT FLUSH':   90000000000,
    'QUADS':   80000000000,
    'FULL HOUSE':       70000000000,
    'FLUSH':            60000000000,
    'STRAIGHT':         50000000000,
    'TRIPS':  40000000000,
    'TWO PAIR':         30000000000,
    'PAIR':             20000000000,
    'HIGH CARD':        0,
    #  'STRAIGHT-FLUSH DRAW': 0,
    #  'FLUSH DRAW':       0,
    #  'STRAIGHT DRAW':    0,
    'INVALID': -1
}


def get_type(value):
    # Determine the hand given the numerical value
    roundedval = round(value, -10)

    for v in HANDTYPES:
        if HANDTYPES[v] == roundedval:
            return v
    else:
        return 'Type error: Cannot find type!'


def get_description(value, cards):
    ranks = sort_ranks(cards)
    ctype = get_type(value)

    if ctype in ['STRAIGHT', 'STRAIGHT FLUSH']:
        if value % 10000000000 == 0:
            return '5 High'
        else:
            #  return '{} High'.format(int((value % 1000000000) / 100000000))
            return '{} High'.format(ranks[0][1])

    elif ctype in ['QUADS', 'TRIPS', 'PAIR']:
        return '{}\'s'.format(ranks[0][1])

    elif ctype == 'FULL HOUSE':
        return '{}\'s full of {}\'s'.format(
            ranks[0][1], ranks[1][1])

    elif ctype == 'TWO PAIR':
        return '{}\'s and {}\'s'.format(
            ranks[0][1], ranks[1][1])

    #  elif ctype in ['FLUSH', 'HIGH CARD']:
    else:
        return '{} High'.format(ranks[0][1])


def is_validhand(cards):
    # Is it a valid poker hand?
    if len(cards) > 5:
        print('INVALID HAND: More than 5 cards!')
        return False
    elif len(cards) < 5:
        print('INVALID HAND: Less than 5 cards!')
        return False
    elif not is_set(cards):
        # Are all the cards unique (and valid)?
        print('INVALID HAND: Contains duplicate cards!')
        return False
    return True


def is_set(cards):
    # Test if a hand contains any duplicate entries
    _cards = cards[:]
    while _cards:
        tempcard = _cards.pop()
        if tempcard in _cards:
            return False
    else:
        return True


def sort_ranks(cards):
    # Build a dictionary of quantity:rank pairs
    ranks = {}
    for c in cards:
        if c.rank in ranks:
            ranks[c.rank] += 1
        else:
            ranks[c.rank] = 1

    # Build a list using value/key pairs
    # Potentially could make into a list comp
    L = []
    for r in ranks:
        L.append((ranks[r], r))

    return sorted(L, key=lambda x: (-x[0], -card.VALUES[x[1]]))


def sort_suits(cards):
    # Build a dictionary of quantity:suit counts
    suits = {}
    for c in cards:
        if c.suit in suits:
            suits[c.suit] += 1
        else:
            suits[c.suit] = 1
    return suits


def score(cards):
    # Hand should be ordered by highest value first, lowest last
    score = 0
    for i, c in enumerate(cards):
        score += card.VALUES[c[1]] * MULTIPLIERS[i]
    return score


def get_value(cards):
    # Calculate the type of hand and return a string descripting the hand and an integer
    # that correspond to its value
    cards = sorted(cards, key=lambda x: card.VALUES[x.rank])
    sorted_values = sort_ranks(cards)

    if len(sorted_values) == 5:
        # Hand cannot contain any pair-type hands
        if is_royal_flush(cards):
            return HANDTYPES['ROYAL FLUSH']
        elif is_straight_flush(cards):
            if cards[0].rank == '2':
                return HANDTYPES['STRAIGHT FLUSH']
            return HANDTYPES['STRAIGHT FLUSH'] \
                + card.VALUES[sorted_values[4][1]] * MULTIPLIERS[0]
        elif is_flush(cards):
            return HANDTYPES['FLUSH'] + score(sorted_values)
        elif is_low_straight(cards):
            return HANDTYPES['STRAIGHT']
        elif is_straight(cards):
            return HANDTYPES['STRAIGHT'] + score(sorted_values)
        else:
            return HANDTYPES['HIGH CARD'] + score(sorted_values)

    elif len(sorted_values) > 1:
        if sorted_values[0][0] == 4:
            return HANDTYPES['QUADS'] + score(sorted_values)
        elif sorted_values[0][0] == 3 and sorted_values[1][0] == 2:
            return HANDTYPES['FULL HOUSE'] + score(sorted_values)
        elif sorted_values[0][0] == 3 and sorted_values[1][0] == 1:
            return HANDTYPES['TRIPS'] + score(sorted_values)
        elif sorted_values[0][0] == 2 and sorted_values[1][0] == 2:
            return HANDTYPES['TWO PAIR'] + score(sorted_values)
        elif sorted_values[0][0] == 2 and sorted_values[1][0] == 1:
            return HANDTYPES['PAIR'] + score(sorted_values)

    return HANDTYPES['INVALID']


def is_royal_flush(cards):
    if is_straight_flush(cards) and cards[0].rank == 'T':
        return True
    else:
        return False


def is_straight_flush(cards):
    if is_straight(cards) and is_flush(cards):
        return True
    elif is_low_straight(cards) and is_flush(cards):
        return True
    else:
        return False


def is_flush(cards):
    if len(cards) > 5:
        ValueError('Hand is too large to measure!')

    suitdict = sort_suits(cards)
    maxsuit = max(suitdict.keys(), key=(lambda k: suitdict[k]))
    return suitdict[maxsuit] == 5


def get_longest_suit(cards):
    suitdict = sort_suits(cards)
    maxsuit = max(suitdict.keys(), key=(lambda k: suitdict[k]))

    # Return both the most common suit and the number of occurrences.
    return maxsuit, suitdict[maxsuit]


def get_gap(card1, card2):
    # Paired cards have no gap
    if card1.rank == card2.rank:
        return -1

    # minus the extra 1 to offset the connectness
    # Example: For 87, 8 - 7 = 1, but the gap is actually 0
    return abs(card1.val() - card2.val()) - 1


def get_allgaps(cards):
    # Determine if all the cards are consecutive ranks
    # (should work regardless of order)

    ordered = sorted(cards)
    gaps = 0

    for i, c in enumerate(ordered):
        if i == len(cards) - 1:
            break
        g = get_gap(ordered[i], ordered[i + 1])
        if g == -1:
            raise ValueError('Pair detected while attempting to parse connected cards!')
        gaps += g
    return gaps


def is_straight(cards):
    if len(cards) != 5:
        return False
    else:
        return get_allgaps(cards) == 0


def is_low_straight(cards):
    # Ace is low
    return cards[0].rank == '2' \
        and cards[1].rank == '3' \
        and cards[2].rank == '4' \
        and cards[3].rank == '5' \
        and cards[4].rank == 'A'


def find_best_hand(cards):
    if len(cards) < 5:
        return None
    hands = [hand.Hand(c) for c in itertools.combinations(cards, 5)]

    besthand = hands[0]

    for h in hands:
        if h.value > besthand.value:
            besthand = h
    return besthand


def pop_ranks(cards, ranks):
    # Remove ALL BUT the rank given.
    discard = []
    for c in cards:
        if c.rank not in ranks:
            discard.append(c)
    return discard


def pop_suits(cards, suit):
    # Remove ALL BUT the suit given.
    discard = []
    for c in cards:
        if c.suit != suit:
            discard.append(c)
    return discard
