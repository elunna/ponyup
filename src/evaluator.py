""" Evaluates poker hands """

from collections import namedtuple
import itertools
from ponyup import card

Ranklist = namedtuple('Ranklist', ['quantity', 'rank'])
HANDSIZE = 5
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


def is_validhand(cards):
    """ Returns True if the cardlist is 5 unique cards. """
    if len(cards) > 5:
        return False
    elif len(cards) < 5:
        return False
    elif not is_set(cards):
        return False
    return True


def dominant_suit(cards):
    """ Finds which suit occurs with the greatest frequency in a list of Cards.
        If there are an equal # of suits between cards, count the higher ranked
        cards.  If a tie is further needed to be broken because the suited cards
        are the same rank, break the tie by using the traditional ranking of suits.
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
    """ Returns True if all the cards in the list match the same suit. """
    suit = cards[0].suit
    for c in cards:
        if c.suit != suit:
            return False
    return True


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


def score_ranklist(ranklist):
    """ Calculates and returns the score of a sorted list of 5 cards.
        Precondition: Hand should be ordered by highest value first, lowest last
    """
    score = 0
    for i, c in enumerate(ranklist):
        score += card.RANKS[c[1]] * MULTIPLIERS[i]
    return score


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
        score += card.RANKS[c.rank] * multiplier
    return score


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
    #  cards = sorted(cards, key=lambda x: card.RANKS[x.rank])
    #  ranklist = rank_list(cards)

    ranklist = rank_list(sorted(cards))

    if len(ranklist) < 5:
        return score_pair_hands(cards)
    elif len(ranklist) == HANDSIZE:
        # Returns the value of a non-pair hand.
        FIVEHIGH, ACEHIGH = 5, 14

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


def is_set(items):
    """ Return False if items contains any duplicate entries and True if they
        are all unique.
    """
    return len(set(items)) == len(items)


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

    return sorted(L, key=lambda x: (-x.quantity, -card.RANKS[x.rank]))


def suit_dict(cards):
    """ Returns a dictionary of quantity/suit pair counts. """
    suits = {}
    for c in cards:
        suits[c.suit] = suits.get(c.suit, 0) + 1
    return suits


def suitedcard_dict(cards):
    """ Returns a dictionary of suits and card lists. Useful for dividing a list
        of cards into all the separate suits.
    """
    suits = {}
    for c in cards:
        key = c.suit
        suits.setdefault(key, []).append(c)  # Dict grouping
    return suits


def count_suit(cards, suit):
    """ Counts how many cards of the given suit occur in the card list. """
    return sum(1 for c in cards if c.suit == suit)


def count_rank(cards, rank):
    """ Counts how many cards of the given rank occur in the card list. """
    return sum(1 for c in cards if c.rank == rank)


def get_gap(card1, card2):
    """ Return how many spaces are between the ranks of 2 cards.
        Example: For 87, 8 - 7 = 1, but the gap is actually 0. Paired cards have no gap.
    """
    if card1.rank == card2.rank:
        return -1

    return abs(card1.val() - card2.val()) - 1


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


def strip_ranks(cards, ranks):
    """ Takes a list of cards, removes the rank(s) given, and returns a list of
        the leftovers.  There can be more than one rank passed.
    """
    return [c for c in cards if c.rank not in ranks]


def strip_suits(cards, suits):
    """ Takes a list of cards, removes the suit given, and returns a list of the
        leftovers. There can only be one suit passed.
    """
    return [c for c in cards if c.suit not in suits]


def chk_wheel(cards):
    """ Check if the group of cards(passed as a rank dictionary) counts as a wheel
        draw. The requirements are that an Ace must be present in the group of
        cards and that all other cards must be no higher than a 5.  There must
        also be no pairs present, otherwise the order of the draw will be disrupted.
    """
    rankdict = rank_dict(cards)
    wheelcards = ['A', '2', '3', '4', '5']
    if 'A' not in rankdict:
        return False
    for k, v in rankdict.items():
        if k not in wheelcards:
            return False
        elif v > 1:
            return False
    return True


def chk_straight_draw(cards, qty, gap):
    """ Check for wheel draws, we should only have to check the first x cards,
        where x is qty-1, because the Ace takes out one card. For this exceptional
        case, we will ignore the gap because wheel draws are inherently gapped
        anyway. We also add this to the draws list first so that if a better draw
        comes up later it will be used instead.
    """
    # Remove any extra pairs first - they interfere with checking straight draws.
    pared = remove_pairs(cards)

    if qty > len(pared):
        raise ValueError('qty cannot be larger than the length of the card list!')

    draws = []

    if max(pared).rank == 'A':
        # Take the low cards and add the Ace (which should be at the end of the sorted list.
        aceslice = pared[0: qty - 1]
        aceslice.append(pared[-1])
        if chk_wheel(aceslice):
            draws.append(aceslice)

    end_index = (len(pared) - qty) + 1
    for i in range(end_index):
        currentslice = pared[i: qty + i]
        if get_allgaps(currentslice) <= gap:
            draws.append(currentslice)
    if draws:
        # Return the highest draw found, which would be the last added.
        return draws[-1]
    else:
        return None


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
