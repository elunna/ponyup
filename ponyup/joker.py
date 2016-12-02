"""
  " Tools for using the Joker in a playing card games.
  """
from ponyup import card
from ponyup import deck
from ponyup import evaluator


def pick_joker(cards):
    """ Picks the best card for the joker to represent for a group of cards.  """
    # If the Joker is in the pile of cards, remove it for analysis.
    if card.JOKER1 in cards:
        cards.remove(card.JOKER1)
    if card.JOKER2 in cards:
        cards.remove(card.JOKER2)

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
