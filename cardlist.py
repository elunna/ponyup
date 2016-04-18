import card


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


def rank_dict(cards):
    ranks = {}
    for c in cards:
        if c.rank in ranks:
            ranks[c.rank] += 1
        else:
            ranks[c.rank] = 1
    return ranks


def rank_list(cards):
    """
    Returns a list of quantity/rank pairs by first making a dictionary
    and then converting it to a list and sorting it by rank.
    """
    ranks = rank_dict(cards)
    L = [(ranks[r], r) for r in ranks]

    return sorted(L, key=lambda x: (-x[0], -card.RANKS[x[1]]))


def suit_dict(cards):
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
    count = 0
    for c in cards:
        if c.suit == suit:
            count += 1
    return count


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


def strip_ranks(cards, ranks):
    """
    Takes a list of cards, removes the rank(s) given, and returns a list of the leftovers.
    There can be more than one rank passed.
    """
    discard = []
    for c in cards:
        if c.rank not in ranks:
            discard.append(c)
    return discard


def strip_suits(cards, suits):
    """
    Takes a list of cards, removes the suit given, and returns a list of the leftovers.
    There can only be one suit passed.
    """
    discard = []
    for c in cards:
        if c.suit not in suits:
            discard.append(c)
    return discard
