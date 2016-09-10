import card
import itertools


def valid_holecards(cards):
    if len(cards) != 2:
        return False
    elif cards[0] == cards[1]:
        return False
    else:
        return True


def card2text(cards):
    if not valid_holecards(cards):
        raise ValueError('Only accepts a list of exactly 2 cards!')

    rankhi = cards[0].rank
    ranklo = cards[1].rank
    suited = cards[0].suit == cards[1].suit

    if rankhi == ranklo:
        # Check for pair
        return str(rankhi) * 2
    elif suited:
        # Check for suited
        return rankhi + ranklo + 's'
    else:
        # Offsuit
        return rankhi + ranklo + 'o'


def text2cards(string):
    if len(string) > 3:
        # Something's wrong.
        pass

    if string[0] == string[1]:
        # Pair
        cards = [card.Card(string[0], s) for s in card.SUITS]
        for c in cards:
            c.hidden = False
        return list(itertools.combinations(cards, 2))

    elif string[2] == 's':
        # Suited cards - only have 4 combos
        combos = []
        for s in card.SUITS:
            combos.append((card.Card(string[0], s), card.Card(string[1], s)))

        return combos

    elif string[2] == 'o':
        # Offsuit cards - 12 combos(suited combos not included)
        rank1 = [card.Card(string[0], s) for s in card.SUITS]
        rank2 = [card.Card(string[1], s) for s in card.SUITS]
        return [(c1, c2) for c1 in rank1 for c2 in rank2 if c1.suit != c2.suit]


def power_index(c):
    if c.rank == 'A':
        return 15
    else:
        return c.val()


def sage_score(cards):
    c1, c2 = sorted(cards)

    score = power_index(c1) + power_index(c2) * 2

    if c1.rank == c2.rank:
        score += 22

    if c1.suit == c2.suit:
        score += 2

    return score
