#!/usr/bin/env python3

from __future__ import print_function
import deck
import hand
import evaluator
import itertools


def get_combos(source, n):
    return itertools.combinations(source, n)


def count_all_handtypes():
    print('#'*80)
    print('')
    print('Counting the hand types in all 5 card combos')
    print('Might take a few moments...')
    type_count = {}

    combosof5 = list(get_combos(d.cards, 5))

    for c in combosof5:
        #  hands.append(hand.Hand(c))
        h = hand.Hand(c)
        rank = h.handrank
        if rank not in type_count:
            type_count[rank] = 1
        else:
            type_count[rank] += 1

    print('')
    print('')
    print('Results:')
    for t in type_count:
        print('{}: {}'.format(t, type_count[t]))


def get_unique_5cardhands():
    # Filter out all the hands that have the same value so we can see how many unique values
    # there are.
    d = deck.Deck()
    print('Creating a dictionary of hand values and hands')
    hands = {}
    for c in get_combos(d.cards, 5):
        h = hand.Hand(c)
        hands[h.value] = h

    print('')
    print('Number of unique hands: {}'.format(len(hands)))

    return hands


def sorted_hands_list(handdict):
    # Sort by value
    sortedhands = []
    for h in handdict:
        sortedhands.append(
            (handdict[h].value, handdict[h].handrank, handdict[h].cards))

    return sorted(sortedhands)


def print_unique_5cardhands(handlist):
    for h in handlist:
        print('{:<15}{:<15}{:<15}'.format(
            h[0], h[1], evaluator.print_cardlist(h[2])))


def print_holdem_startinghands():
    for c in list(get_combos(d.cards, 2)):
        print('[{}] '.format(evaluator.print_cardlist(c)))


def get_combos_all_sizes(cards):
    combos = []
    for i in range(1, 6):
        for c in list(get_combos(cards, i)):
            combos.append(c)
        #  combos.append(list(get_combos(cards, i)))
        #  combos.append(list(get_combos(cards, i)))
    return combos


def n_choose_k(n, k):
    if n < 0 or k < 0:
        raise ValueError('Value passed is below 0!')
    elif k > n:
        raise ValueError('pick is larger than quantity of objects!')

    numerator = [x for x in range(1, n + 1)]

    diff = n - k
    denominator = [x for x in range(1, diff + 1)]
    denominator.extend([x for x in range(1, k + 1)])

    #  print('starting lists')
    #  print(numerator)
    #  print('/')
    #  print(denominator)
    #  print('duplicates')
    #  print(set(numerator) & set(denominator))
    dups = list(set(numerator) & set(denominator))
    for d in dups:
        numerator.remove(d)
        denominator.remove(d)

    #  print('After removing duplicates')
    #  print(numerator)
    #  print('/')
    #  print(denominator)

    numproduct, denproduct = 1, 1
    for n in numerator:
        numproduct *= n
    for n in denominator:
        denproduct *= n

    return int(numproduct / denproduct)


def view_combo_counts():
    d = deck.Deck()
    print('Generating all combos for a standard 52-card deck:')
    combosof1 = list(get_combos(d.cards, 1))
    print('Total combos of 1 card: {}'.format(len(combosof1)))

    combosof2 = list(get_combos(d.cards, 2))
    # Verified there should be 1326 2 card combos
    print('Total combos of 2 cards: {}'.format(len(combosof2)))

    combosof3 = list(get_combos(d.cards, 3))
    # Verified there should be 22100 2 card combos
    print('Total combos of 3 cards: {}'.format(len(combosof3)))

    combosof4 = list(get_combos(d.cards, 4))
    # Not verified yet.
    print('Total combos of 4 cards: {}'.format(len(combosof4)))

    combosof5 = list(get_combos(d.cards, 5))
    # Verified there should be 25989602 card combos
    print('Total combos of 5 cards: {}'.format(len(combosof5)))


if __name__ == "__main__":
    print('#'*80)
    print('')
    print('Combo tests')

    d = deck.Deck()
    # Warning, takes a while!
    # 01/25/16: Verified that the counts are all exactly correct.
    print('*'*80)
    print('Counting all 5 card hands in a deck')
    count_all_handtypes()

    print('*'*80)
    print('Enumerating unique 5-card hands by value')
    unique_hands = get_unique_5cardhands()
    sortedhands = sorted_hands_list(unique_hands)
    print_unique_5cardhands(sortedhands)

    print('*'*80)
    print('Display all holdem starting hands.')
    print_holdem_startinghands()
