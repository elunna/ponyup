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
