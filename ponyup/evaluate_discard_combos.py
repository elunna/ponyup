#!/usr/bin/env python3
from ponyup import combos
from ponyup import deck
from ponyup import evaluator
from ponyup import tools

# Minimum rank threshold to reach for improvement
#  RANK = tools.PAIR_JJ
#  RANK = tools.TWOPAIR_22
#  RANK = tools.STRAIGHT
RANK = tools.TRIPS


def find_best_discard(cards):
    # Create a new deck
    d = deck.Deck()

    # Remove the cards in the card list from the deck
    d.remove_cards(cards)
    d.unhide()
    print(d)
    print('deck is length {}'.format(len(d)))

    # Find all discard combos in the card list and assign them to tuples.
    discard_combos = combos.get_allcombos(cards)

    bestdiscard = []  # Keeps track of the best discard combo found.
    bestchance = 0  # Keeps track of the best percent of improvement found.

    # Go through all discard combos:
    for dc in discard_combos:
        print(dc)

        # Discard those cards from the original hand
        hand = rm_discards(cards, dc)

        # N is the number of discards.
        N = len(dc)

        # Get ALL complementary combos of length N from the deck.
        redraw_combos = combos.get_combolist(d.cards, N)

        improves = 0

        #  print('Redraw combos: {}'.format(redraw_combos))
        #  print('Redraw qty: {}'.format(len(redraw_combos)))
        #  print('hand {}'.format(hand))
        #  input('...')

        # Find how many combos improve the value of the hand to the threshold.
        for r in redraw_combos:
            #  print('R = {}'.format(r))
            newhand = hand[:]
            newhand.extend(list(r))

            #  print('newhand {}'.format(newhand))
            #  print(newhand)

            if evaluator.get_value(newhand) > RANK:
                improves += 1

            chance_of_improvement = improves / len(redraw_combos)
            if chance_of_improvement > bestchance:
                bestchance = chance_of_improvement
                bestdiscard = dc

    # Find the discard combo that has the highest change of improving to the rank threshold.
    return bestdiscard, bestchance


def rm_discards(cards, discards):
    cards = cards[:]
    for x in discards:
        cards.remove(x)
    return cards

if __name__ == "__main__":
    h = tools.make('OESD', hidden=False)
    print(h)
    d, c = find_best_discard(h)

    print('The best discard for {} is {}.'.format(h, d))
    print('There is a {}% chance of improving to {} or better'.format(
        c, evaluator.get_type(RANK)))
