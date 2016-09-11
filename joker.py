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
    if card.JOKER1 in cards:
        cards.remove(card.JOKER1)
    if card.JOKER2 in cards:
        cards.remove(card.JOKER2)

    if len(cards) != 4:
        raise Exception('Cards should be a group of 4 cards!')

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
