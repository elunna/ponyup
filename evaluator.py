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


def get_type(value):
    """
    # Determine the type of hand given the numerical value
    """
    if value < 0:
        raise ValueError('get_type() cannot accept negative numbers!')
    else:
        roundedval = round(value, -10)

    for v in HANDTYPES:
        if HANDTYPES[v] == roundedval:
            return v
    else:
        raise ValueError('Type error: Cannot find type!')


def get_description(value, cards):
    """
    Returns a fitting text description of the passed pokerhand.

    Note: May want to refactor to only take a list of cards.
    """
    ranks = sort_ranks(cards)
    ctype = get_type(value)

    if ctype in ['STRAIGHT', 'STRAIGHT FLUSH']:
        if value % 10000000000 == 0:
            return '5 High'
        else:
            return '{} High'.format(ranks[0][1])
    elif ctype in ['QUADS', 'TRIPS', 'PAIR']:
        return '{}\'s'.format(ranks[0][1])
    elif ctype == 'FULL HOUSE':
        return '{}\'s full of {}\'s'.format(
            ranks[0][1], ranks[1][1])
    elif ctype == 'TWO PAIR':
        return '{}\'s and {}\'s'.format(
            ranks[0][1], ranks[1][1])
    else:
        return '{} High'.format(ranks[0][1])


def is_validhand(cards):
    """
    Returns True if the cardlist is 5 unique cards."
    """
    if len(cards) > 5:
        return False
    elif len(cards) < 5:
        return False
    elif not is_set(cards):
        return False
    return True


def is_set(itemlist):
    """
    Return False if a list contains any duplicate entries and True if they are all unique.
    """
    items = itemlist[:]
    while items:
        i = items.pop()
        if i in items:
            return False
    else:
        return True


def sort_ranks(cards):
    """
    Returns a list of quantity/rank pairs by first making a dictionary
    and then converting it to a list and sorting it by rank.
    Note: Potentially could make into a list comp
    """
    ranks = {}
    for c in cards:
        if c.rank in ranks:
            ranks[c.rank] += 1
        else:
            ranks[c.rank] = 1

    L = []
    for r in ranks:
        L.append((ranks[r], r))

    return sorted(L, key=lambda x: (-x[0], -card.RANKS[x[1]]))


def sort_suits(cards):
    """
    # Returns a dictionary of quantity/suit pair counts.
    """
    suits = {}
    for c in cards:
        if c.suit in suits:
            suits[c.suit] += 1
        else:
            suits[c.suit] = 1
    return suits


def score(cards):
    """
    Calculates and returns the score of a sorted list of 5 cards.
    Precondition:  Hand should be ordered by highest value first, lowest last
    """
    score = 0
    for i, c in enumerate(cards):
        score += card.RANKS[c[1]] * MULTIPLIERS[i]
    return score


def get_value(cards):
    """
    Calculate the type of hand and return its integer value.
    """
    cards = sorted(cards, key=lambda x: card.RANKS[x.rank])
    sorted_values = sort_ranks(cards)

    if len(sorted_values) == 5:
        # Non pair-type hands
        if is_flush(cards):
            if is_straight(cards):
                if cards[0].rank == 'T':
                    return HANDTYPES['ROYAL FLUSH']
                elif cards[0].rank == '2':
                    return HANDTYPES['STRAIGHT FLUSH']
                else:
                    return HANDTYPES['STRAIGHT FLUSH'] \
                        + card.RANKS[sorted_values[4][1]] * MULTIPLIERS[0]
            else:
                return HANDTYPES['FLUSH'] + score(sorted_values)
        elif is_straight(cards):
            if cards[0].rank == '2':
                return HANDTYPES['STRAIGHT']
            else:
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


def get_longest_suit(cards):
    """
    Looks at all the cards in a list and finds which suit occurs with the greatest
    frequency. Returns the suit and number of occurences.
    """
    suitdict = sort_suits(cards)
    maxsuit = max(suitdict.keys(), key=(lambda k: suitdict[k]))

    # Return both the most common suit and the number of occurrences.
    return maxsuit, suitdict[maxsuit]


def get_gap(card1, card2):
    """
    Looks at 2 cards and finds how far apart their ranks are.
    """
    # Paired cards have no gap
    if card1.rank == card2.rank:
        return -1

    # minus the extra 1 to offset the connectness
    # Example: For 87, 8 - 7 = 1, but the gap is actually 0
    return abs(card1.val() - card2.val()) - 1


def get_allgaps(cards):
    """
    Takes a list of cards and determines how many gaps are between all the ranks (when
    they occur in sorted order.
    # Should work regardless of order
    """

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


def find_best_hand(cards):
    """
    Takes a list of cards and determines the best available 5 card hand and returns that
    hand as a Hand.
    """
    if len(cards) < 5:
        return None
    hands = [hand.Hand(c) for c in itertools.combinations(cards, 5)]

    besthand = hands[0]

    for h in hands:
        if h.value > besthand.value:
            besthand = h
    return besthand


def pop_ranks(cards, ranks):
    """
    Takes a list of cards and removes ALL BUT the rank(s) given.
    There can be more than one rank passed.
    """
    discard = []
    for c in cards:
        if c.rank not in ranks:
            discard.append(c)
    return discard


def pop_suits(cards, suit):
    """
    Takes a list of cards and removes ALL BUT the suit given.
    There can only be one suit passed.
    """
    discard = []
    for c in cards:
        if c.suit != suit:
            discard.append(c)
    return discard


def is_flush(cards):
    """
    Returns True if the hand is a flush, False otherwise.
    """

    if len(cards) > 5:
        ValueError('Hand is too large to measure!')

    suitdict = sort_suits(cards)
    maxsuit = max(suitdict.keys(), key=(lambda k: suitdict[k]))
    return suitdict[maxsuit] == 5


def is_straight(cards):
    """
    Returns True if the hand is a straight, False otherwise.
    """
    if len(cards) != 5:
        return False

    elif cards[0].rank == '2' \
            and cards[1].rank == '3' \
            and cards[2].rank == '4' \
            and cards[3].rank == '5' \
            and cards[4].rank == 'A':
        return True
    else:
        return get_allgaps(cards) == 0
