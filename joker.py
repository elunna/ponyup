import card
import deck
import evaluator

JOKER1 = card.Card('Z', 's')
JOKER2 = card.Card('Z', 'c')


def pick_joker(cards):
    """
    Picks the best card for the joker to represent for a group of cards.
    """
    # If the Joker is in the pile of cards, remove it for analysis.
    if JOKER1 in cards:
        cards.remove(JOKER1)
    if JOKER2 in cards:
        cards.remove(JOKER2)

    if len(cards) > 4:
        raise ValueError('Hand is too large to analyze for joker. Must be 1-4 without joker.')

    d = deck.Deck()
    d.unhide()
    bestvalue = 0
    bestcard = None

    for c in d.cards:
        testhand = cards[:]
        testhand.append(c)
        test_val = evaluator.get_value(testhand)

        if test_val > bestvalue:
            bestvalue = test_val
            bestcard = c
    return bestcard
