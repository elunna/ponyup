#!/usr/bin/env python
""" Evaluates poker hands """

from __future__ import print_function
import card
import hand
import itertools

#  MULTIPLIERS = (1, 100, 10000, 1000000, 100000000)
MULTIPLIERS = (100000000, 1000000, 10000, 100, 1)

HANDTYPES = {
    #                   100000000   # Largest multiplier
    'ROYAL FLUSH':      100000000000,
    'STRAIGHT FLUSH':   90000000000,
    'FOUR OF A KIND':   80000000000,
    'FULL HOUSE':       70000000000,
    'FLUSH':            60000000000,
    'STRAIGHT':         50000000000,
    'THREE OF A KIND':  40000000000,
    'TWO PAIR':         30000000000,
    'PAIR':             20000000000,
    'HIGH CARD':        0,
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


def is_validhand(hand):
    # Is it a valid poker hand?
    if len(hand) > 5:
        print('INVALID HAND: More than 5 cards!')
        return False
    elif len(hand) < 5:
        print('INVALID HAND: Less than 5 cards!')
        return False
    elif not is_set(hand):
        # Are all the cards unique (and valid)?
        print('INVALID HAND: Contains duplicate cards!')
        return False
    return True


def is_set(hand):
    # Test if a hand contains any duplicate entries
    handcopy = [c for c in hand.cards]
    while handcopy:
        tempcard = handcopy.pop()
        if tempcard in handcopy:
            return False
    else:
        return True


def sort_ranks(hand):
    # Build a dictionary of quantity:rank pairs
    ranks = {}
    for c in hand:
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


def sort_suits(hand):
    # Build a dictionary of quantity:suit counts
    suits = {}
    for c in hand:
        if c.suit in suits:
            suits[c.suit] += 1
        else:
            suits[c.suit] = 1
    return suits


def score(hand):
    # Hand should be ordered by highest value first, lowest last
    score = 0
    for i, c in enumerate(hand):
        score += card.VALUES[c[1]] * MULTIPLIERS[i]
    return score

    # card.VALUES[sorted_values[0][1]] * MULTIPLIERS[4] +\


def get_value(hand):
    # Calculate the type of hand and return a string descripting the hand and an integer
    # that correspond to its value
    #  value_dict = counted_dict(hand)
    hand = sorted(hand, key=lambda x: card.VALUES[x.rank])
    sorted_values = sort_ranks(hand)

    if len(sorted_values) == 5:
        # Hand cannot contain any pair-type hands
        if is_royal_flush(hand):
            return HANDTYPES['ROYAL FLUSH']
        elif is_straight_flush(hand):
            if hand[0].rank == '2':
                return HANDTYPES['STRAIGHT FLUSH']
            return HANDTYPES['STRAIGHT FLUSH'] \
                + card.VALUES[sorted_values[4][1]] * MULTIPLIERS[0]
        elif is_flush(hand):
            return HANDTYPES['FLUSH'] + score(sorted_values)
        elif is_low_straight(hand):
            return HANDTYPES['STRAIGHT']
        elif is_straight(hand):
            return HANDTYPES['STRAIGHT'] + score(sorted_values)
        else:
            return HANDTYPES['HIGH CARD'] + score(sorted_values)

    elif len(sorted_values) > 1:
        if sorted_values[0][0] == 4:
            return HANDTYPES['FOUR OF A KIND'] + score(sorted_values)
        elif sorted_values[0][0] == 3 and sorted_values[1][0] == 2:
            return HANDTYPES['FULL HOUSE'] + score(sorted_values)
        elif sorted_values[0][0] == 3 and sorted_values[1][0] == 1:
            return HANDTYPES['THREE OF A KIND'] + score(sorted_values)
        elif sorted_values[0][0] == 2 and sorted_values[1][0] == 2:
            return HANDTYPES['TWO PAIR'] + score(sorted_values)
        elif sorted_values[0][0] == 2 and sorted_values[1][0] == 1:
            return HANDTYPES['PAIR'] + score(sorted_values)

    return HANDTYPES['INVALID']


def is_royal_flush(hand):
    if is_straight_flush(hand) and hand[0].rank == 'T':
        return True
    else:
        return False


def is_straight_flush(hand):
    if is_straight(hand) and is_flush(hand):
        return True
    elif is_low_straight(hand) and is_flush(hand):
        return True
    else:
        return False

"""
def is_flush(hand):
    suit = hand[0].suit
    for c in hand:
        if c.suit != suit:
            return False
    return True
"""


def is_flush(hand):
    if len(hand) > 5:
        ValueError('Hand is too large to measure!')

    return count_suited(hand) == 5


def count_suited(hand):
    #  print_cardlist(hand)
    suitdict = sort_suits(hand)
    #  print(suitdict)
    for i in range(13, 1, -1):
        if i in suitdict.values():
            return i
    print('Suit counting error!')


# Assumes the hand is sorted
def is_straight(hand):
    #  return hand[4].val() < hand[0].val() + 4
    return hand[0].val() == hand[1].val() - 1 \
        and hand[1].val() == hand[2].val() - 1 \
        and hand[2].val() == hand[3].val() - 1 \
        and hand[3].val() == hand[4].val() - 1


def is_low_straight(hand):
    # Ace is low
    return hand[0].rank == '2' \
        and hand[1].rank == '3' \
        and hand[2].rank == '4' \
        and hand[3].rank == '5' \
        and hand[4].rank == 'A'


def find_best_hand(cards):
    if len(cards) < 5:
        return None
    hands = [hand.Hand(c) for c in itertools.combinations(cards, 5)]

    besthand = hands[0]

    for h in hands:
        if h.value > besthand.value:
            besthand = h
    return besthand


def print_cardlist(cards):
    display = ''
    for c in cards:
        display += '{} '.format(str(c))
    return display


"""
def print_list(mylist):
    for i in mylist:
        print(i)

"""
