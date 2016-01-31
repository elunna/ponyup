#!/usr/bin/env python
""" Evaluates poker hands """

from __future__ import print_function
import card
import hand
import itertools

MULTIPLIERS = (
    1,
    100,
    10000,
    1000000,
    100000000)

VALUES = {
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
    #  print('hand value: {}'.format(value))
    #  print('value % 1000000: {}'.format(value % 1000000))
    #  print('value / 1000000: {}'.format(value / 1000000))
    #  print('round(value, -1): {}'.format(round(value, -1)))
    #  print('round(value, -2): {}'.format(round(value, -2)))
    #  print('round(value, -3): {}'.format(round(value, -3)))
    #  print('round(value, -4): {}'.format(round(value, -4)))
    #  print('round(value, -5): {}'.format(round(value, -5)))
    roundedval = round(value, -10)
    #  print('Rounded value: {}'.format(roundedval))

    for v in VALUES:
        if VALUES[v] == roundedval:
            return v
    else:
        return 'Type error: Cannot find type!'


def valid_hand(hand):
    # Is it 5 cards?
    if len(hand) > 5:
        print('INVALID HAND: More than 5 cards!')
        return False
    elif len(hand) < 5:
        print('INVALID HAND: Less than 5 cards!')
        return False
    #  elif len(set(hand.cards)) < 5:
    elif not is_set(hand):
        print('INVALID HAND: Contains duplicate cards!')
        return False
    # Are all the cards unique (and valid)?
    #  print('Valid hand!')
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


def counted_dictionary(hand):
    ranks = {}
    for c in hand:
        if c.rank in ranks:
            ranks[c.rank] += 1
        else:
            ranks[c.rank] = 1
    return ranks


def sort_dict_values(dictionary):
    # Build a list using value/key pairs
    # Potentially could make into a list comp
    L = []
    for r in dictionary:
        L.append((dictionary[r], r))

    return sorted(L, key=lambda x: (-x[0], -card.cardvalues[x[1]]))


def score(hand):
    score = 0
    for i in range(5):
        score += hand[i].val() * MULTIPLIERS[i]
    return score


def get_value(hand):
    # Calculate the type of hand and return a string descripting the hand and an integer
    # that correspond to its value
    value_dict = counted_dictionary(hand)
    L = sort_dict_values(value_dict)
    hand = sorted(hand, key=lambda x: card.cardvalues[x.rank])

    #  print('sorted hand: ', end='')
    #  print_hand(hand)

    if len(value_dict) == 5:
        # Hand cannot contain any pair-type hands
        if is_royal_flush(hand):
            return VALUES['ROYAL FLUSH']
        elif is_straight_flush(hand):
            if hand[0].rank == '2':
                return VALUES['STRAIGHT FLUSH']
            return VALUES['STRAIGHT FLUSH'] + MULTIPLIERS[4] * hand[4].val()
        elif is_flush(hand):
            return VALUES['FLUSH'] + score(hand)
        elif is_low_straight(hand):
            return VALUES['STRAIGHT']
        elif is_straight(hand):
            return VALUES['STRAIGHT'] + score(hand)
        else:
            return VALUES['HIGH CARD'] + score(hand)

    elif len(value_dict) > 1:
        if L[0][0] == 4:
            return VALUES['FOUR OF A KIND'] +\
                card.cardvalues[L[0][1]] * MULTIPLIERS[4] +\
                card.cardvalues[L[1][1]] * MULTIPLIERS[3]

        elif L[0][0] == 3 and L[1][0] == 2:
            return VALUES['FULL HOUSE'] +\
                card.cardvalues[L[0][1]] * MULTIPLIERS[4] +\
                card.cardvalues[L[1][1]] * MULTIPLIERS[3]

        elif L[0][0] == 3 and L[1][0] == 1:
            return VALUES['THREE OF A KIND'] +\
                card.cardvalues[L[0][1]] * MULTIPLIERS[4] +\
                card.cardvalues[L[1][1]] * MULTIPLIERS[3] +\
                card.cardvalues[L[2][1]] * MULTIPLIERS[2]

        elif L[0][0] == 2 and L[1][0] == 2:
            return VALUES['TWO PAIR'] +\
                card.cardvalues[L[0][1]] * MULTIPLIERS[4] +\
                card.cardvalues[L[1][1]] * MULTIPLIERS[3] +\
                card.cardvalues[L[2][1]] * MULTIPLIERS[2]

        elif L[0][0] == 2 and L[1][0] == 1:
            return VALUES['PAIR'] +\
                card.cardvalues[L[0][1]] * MULTIPLIERS[4] +\
                card.cardvalues[L[1][1]] * MULTIPLIERS[3] +\
                card.cardvalues[L[2][1]] * MULTIPLIERS[2] +\
                card.cardvalues[L[3][1]] * MULTIPLIERS[1]

    return VALUES['INVALID']


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


def is_flush(hand):
    suit = hand[0].suit
    for c in hand:
        if c.suit != suit:
            return False
    return True


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


def print_list(mylist):
    for i in mylist:
        print(i)


def print_cardlist(hand):
    display = ''
    for c in hand:
        #  print('{} '.format(str(c)), end='')
        display += '{} '.format(str(c))
    return display


def get_combos(source, n):
    return itertools.combinations(source, n)


def find_best_hand(cards):
    if len(cards) < 5:
        return None
    hands = [hand.Hand(c) for c in get_combos(cards, 5)]

    besthand = hands[0]

    for h in hands:
        if h.value > besthand.value:
            besthand = h
    return besthand
