#!/usr/bin/env python3

from __future__ import print_function
import deck
import hand
import evaluator
import itertools


def n_choose_k(n, k):
    if n <= 0 or k <= 0:
        raise ValueError('N or K passed is less than or equal to 0!')
    elif k > n:
        raise ValueError('Pick is larger than quantity of objects!')

    numerator = [x for x in range(1, n + 1)]

    diff = n - k
    denominator = [x for x in range(1, diff + 1)]
    denominator.extend([x for x in range(1, k + 1)])

    dups = list(set(numerator) & set(denominator))
    for d in dups:
        numerator.remove(d)
        denominator.remove(d)

    numproduct, denproduct = 1, 1
    for n in numerator:
        numproduct *= n

    for n in denominator:
        denproduct *= n

    return int(numproduct / denproduct)


def get_combolist(cards, n):
    """
    Takes a list of cards and returns a list of all the combinations of size n
    """
    return list(itertools.combinations(cards, n))


def tally_handtypes(handlist):
    """
    Takes in a list of hands and counts all the occurences of each type of hand and tallies
    it up in a dictionary. Returns the dictionary.
    """
    type_count = {}

    for c in combosof5:
        #  hands.append(hand.Hand(c))
        h = hand.Hand(c)
        rank = h.handrank
        if rank not in type_count:
            type_count[rank] = 1
        else:
            type_count[rank] += 1

    return type_count


def display_handtypes(type_count):
    print('Results:')
    for t in type_count:
        print('{}: {}'.format(t, type_count[t]))


def get_unique_5cardhands():
    # Filter out all the hands that have the same value so we can see how many unique values
    # there are.
    d = deck.Deck()
    hands = {}

    # Run through all combinations of 5 card hands
    for c in get_combolist(d.cards, 5):
        #  h = hand.Hand(c)
        v = evaluator.get_value(c)
        #  hands[h.value] = h
        hands[v] = c

    return len(hands)


def sort_handslist(handdict):
    """
    Takes a list of Hands and returns a list sorted by value.
    """
    # Sort by value
    sortedhands = []
    for h in handdict:
        sortedhands.append((handdict[h].value, handdict[h].handrank, handdict[h].cards))

    return sorted(sortedhands)


def print_unique_5cardhands(handlist):
    for h in handlist:
        print('{:<15}{:<15}{:<15}'.format(
            h[0], h[1], evaluator.print_cardlist(h[2])))


def get_combos_all_sizes(cards):
    combos = []
    maxsize = len(cards) + 1
    for i in range(1, maxsize):
        for c in list(get_combolist(cards, i)):
            combos.append(c)
    return combos



if __name__ == "__main__":
    print('Combo tests')

    d = deck.Deck()
    print('Counting all 5 card hands in a deck')

    combosof5 = list(get_combolist(d.cards, 5))
    tally_handtypes(combosof5)

    print('*'*80)
    print('Enumerating unique 5-card hands by value')
    unique_hands = get_unique_5cardhands()
    sortedhands = sort_handslist(unique_hands)
    print_unique_5cardhands(sortedhands)

    print('*'*80)
    print('Display all holdem starting hands.')
    display_holdem_startinghands()
