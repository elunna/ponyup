#!/usr/bin/env python
""" Evaluates poker hands """

from __future__ import print_function
from collections import namedtuple
import card
import hand
import numbers
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
    elif not is_set(cards):
        return False
    return True


def dominant_suit(cards):
    """
    Finds which suit occurs with the greatest frequency in a list of Cards. If there are an
    equal # of suits between cards, count the higher ranked cards.  If a tie is further needed
    to be broken because the suited cards are the same rank, break the tie by using the
    traditional ranking of suits.
    """
    # First create a dictionary to count the suits
    suitdict = suitedcard_dict(cards)

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
    elif get_allgaps(cards) == 0:
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
    sortedranks = rank_list(cards)

    if len(sortedranks) == 5:
        return process_nonpairhands(cards, sortedranks)
    elif len(sortedranks) >= 1:
        return process_pairhands(sortedranks)
    else:
        return HANDTYPES['INVALID']


def get_description(value, cards):
    """
    Returns a fitting text description of the passed pokerhand.
    """
    ranks = rank_list(cards)
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
    """
    Returns the value of a non-pair hand.
    """
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
    """
    Returns the value of a pair-type hand.
    """
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
        if h.value() > besthand.value():
            besthand = h
    return besthand


def is_set(items):
    """
    Return False if items contains any duplicate entries and True if they are all unique.
    """
    return len(set(items)) == len(items)


def rank_dict(cards):
    """
    Returns a dictionary of rank/counts for the list of cards.
    """
    ranks = {}
    for c in cards:
        if c.rank in ranks:
            ranks[c.rank] += 1
        else:
            ranks[c.rank] = 1
    return ranks


def rank_list(cards):
    """
    Returns a list of quantity/rank pairs by making a rank dictionary, converting it to a list
    and sorting it by rank.
    """
    Ranklist = namedtuple('Ranklist', ['quantity', 'rank'])
    ranks = rank_dict(cards)
    L = [Ranklist(quantity=ranks[r], rank=r) for r in ranks]

    return sorted(L, key=lambda x: (-x.quantity, -card.RANKS[x.rank]))


def suit_dict(cards):
    """
    Returns a dictionary of quantity/suit pair counts.
    """
    suits = {}
    for c in cards:
        if c.suit in suits:
            suits[c.suit] += 1
        else:
            suits[c.suit] = 1
    return suits


def suitedcard_dict(cards):
    """
    Returns a dictionary of suits and card lists. Useful for dividing a list of cards
    into all the separate suits.
    """
    suits = {}
    for c in cards:
        if c.suit in suits:
            suits[c.suit].append(c)
        else:
            suits[c.suit] = []
            suits[c.suit].append(c)
    return suits


def count_suit(cards, suit):
    """
    Counts how many cards of the given suit occur in the card list.
    """
    count = 0
    for c in cards:
        if c.suit == suit:
            count += 1
    return count


def get_gap(card1, card2):
    """
    Return how many spaces are between the ranks of 2 cards.
    Example: For 87, 8 - 7 = 1, but the gap is actually 0. Paired cards have no gap.
    """
    if card1.rank == card2.rank:
        return -1

    return abs(card1.val() - card2.val()) - 1


def get_allgaps(cards):
    """
    Takes a list of cards and determines how many gaps are between all the ranks (when
    they occur in sorted order. Should work regardless of order
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


def strip_ranks(cards, ranks):
    """
    Takes a list of cards, removes the rank(s) given, and returns a list of the leftovers.
    There can be more than one rank passed.
    """
    return [c for c in cards if c.rank not in ranks]


def strip_suits(cards, suits):
    """
    Takes a list of cards, removes the suit given, and returns a list of the leftovers.
    There can only be one suit passed.
    """
    return [c for c in cards if c.suit not in suits]


def is_integer(num):
    """
    Determines if the variable is an integer.
    """
    return isinstance(num, numbers.Integral)


def check_draw(cards, qty, gap):
    """
    Check if there is a straight draw in the list of cards. Can specify how many cards the
    straight draw is and how many gaps are acceptable.
    """
    # Assume cards are sorted
    for i in range((len(cards) - qty) + 1):
        if get_allgaps(cards[i: qty + i]) <= gap:
            return cards[i: qty + i]
    else:
        return None


def extract_discards(cards, keep):
    """
    Returns the cards we should discard from a group of cards.
    """
    return [c for c in cards if c not in keep]


def to_card(string):
    if len(string) != 2:
        raise Exception('String must be exactly 2 characters to convert to a card!')
    return card.Card(string[0], string[1])


def convert_to_cards(cardlist):
    return [to_card(x) for x in cardlist]
