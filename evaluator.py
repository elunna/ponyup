#!/usr/bin/env python
""" Evaluates poker hands """

from __future__ import print_function
import card
import cardlist
import hand
import itertools

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


def is_validhand(cards):
    """
    Returns True if the cardlist is 5 unique cards."
    """
    if len(cards) > 5:
        return False
    elif len(cards) < 5:
        return False
    elif not cardlist.is_set(cards):
        return False
    return True


def dominant_suit(cards):
    """
    Looks at all the cards in a list and finds which suit occurs with the greatest
    frequency. If there are an equal # of suits between cards, count the higher ranked cards.
    If a tie is further needed to be broken because the suited cards are the same rank,
    break the tie by using the traditional ranking of suits.
    """

    # First create a dictionary to count the suits
    suitdict = cardlist.suitedcard_dict(cards)

    domcount = 0

    # Find the count of the most dominant suit in the list.
    for s in suitdict:
        cardsofsuit = len(suitdict[s])
        if cardsofsuit > domcount:
            domcount = cardsofsuit

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


def is_suited(cards):
    """
    Returns True if all the cards in the list match the same suit.
    """
    suit = cards[0].suit
    for c in cards:
        if c.suit != suit:
            return False
    return True


def is_straight(cards):
    """
    Returns True if the hand is a straight, False otherwise.
    """
    if not is_validhand(cards):
        return False
    elif cardlist.get_allgaps(cards) == 0:
        return True
    cards = sorted(cards)
    return cards[0].rank == '2' \
        and cards[1].rank == '3' \
        and cards[2].rank == '4' \
        and cards[3].rank == '5' \
        and cards[4].rank == 'A'


def score_ranklist(ranklist):
    """
    Calculates and returns the score of a sorted list of 5 cards.
    Precondition:  Hand should be ordered by highest value first, lowest last
    """
    score = 0
    for i, c in enumerate(ranklist):
        score += card.RANKS[c[1]] * MULTIPLIERS[i]
    return score


def score_cardlist(cards):
    """
    Calculates and returns the score of a sorted list of 5 cards.
    Precondition:  Hand should be ordered by highest value first, lowest last
    """
    score = 0
    for i, c in enumerate(sorted(cards)):
        if i > 0:
            multiplier = 10 ** (i * 2)
        else:
            multiplier = 1
        score += card.RANKS[c.rank] * multiplier
    return score


def get_type(value):
    """
    # Determine the type of hand given the numerical value
    """
    if value < 0:
        return 'INVALID'
    else:
        roundedval = round(value, -10)

    for v in HANDTYPES:
        if HANDTYPES[v] == roundedval:
            return v
    else:
        raise ValueError('Type error: Cannot find type!')


def get_value(cards):
    """
    Calculate the type of hand and return its integer value.
    """
    cards = sorted(cards, key=lambda x: card.RANKS[x.rank])
    sortedranks = cardlist.rank_list(cards)

    if len(sortedranks) == 5:
        return process_nonpairhands(cards, sortedranks)
    elif len(sortedranks) >= 1:
        return process_pairhands(sortedranks)
    else:
        return HANDTYPES['INVALID']


def get_description(value, cards):
    """
    Returns a fitting text description of the passed pokerhand.

    Note: May want to refactor to only take a list of cards.
    """
    ranks = cardlist.rank_list(cards)
    ctype = get_type(value)

    if len(cards) == 0:
        return 'No cards!'
    elif ctype in ['STRAIGHT', 'STRAIGHT FLUSH']:
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


def process_nonpairhands(cards, sortedranks):
    # Non pair-type hands
    if is_suited(cards):
        if is_straight(cards):
            if cards[0].rank == 'T':
                return HANDTYPES['ROYAL FLUSH']
            elif cards[0].rank == '2':
                return HANDTYPES['STRAIGHT FLUSH']
            else:
                return HANDTYPES['STRAIGHT FLUSH'] \
                    + card.RANKS[sortedranks[4][1]] * MULTIPLIERS[0]
        else:
            return HANDTYPES['FLUSH'] + score_ranklist(sortedranks)
    elif is_straight(cards):
        if cards[0].rank == '2':
            return HANDTYPES['STRAIGHT']
        else:
            return HANDTYPES['STRAIGHT'] + score_ranklist(sortedranks)
    else:
        return HANDTYPES['HIGH CARD'] + score_ranklist(sortedranks)


def process_pairhands(ranks):
    if len(ranks) > 1:
        if ranks[0][0] == 3 and ranks[1][0] == 2:
            return HANDTYPES['FULL HOUSE'] + score_ranklist(ranks)
        elif ranks[0][0] == 2 and ranks[1][0] == 2:
            return HANDTYPES['TWO PAIR'] + score_ranklist(ranks)

    if ranks[0][0] == 1:
        return HANDTYPES['HIGH CARD'] + score_ranklist(ranks)
    elif ranks[0][0] == 2:
        return HANDTYPES['PAIR'] + score_ranklist(ranks)
    elif ranks[0][0] == 3:
        return HANDTYPES['TRIPS'] + score_ranklist(ranks)
    elif ranks[0][0] == 4:
        return HANDTYPES['QUADS'] + score_ranklist(ranks)


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
