#!/usr/bin/env python3

from __future__ import print_function
import deck
import evaluator
import itertools
import pickle


def n_choose_k(n, k):
    """
    Returns how many combos of k are in a group of n.
    """
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


def get_allcombos(items):
    """
    Returns all combos of all possible sizes in the given list.
    """
    combos = []
    maxsize = len(items) + 1
    for i in range(1, maxsize):
        for c in list(get_combolist(items, i)):
            combos.append(c)
    return combos


def typecount_dict(handlist):
    """
    Takes in a list of hands and counts all the occurences of each type of hand and tallies
    it up in a dictionary. Returns the dictionary.
    """
    type_count = {}

    for c in handlist:
        v = evaluator.get_value(c)
        t = evaluator.get_type(v)
        #  h = hand.Hand(c)
        #  rank = h.rank()
        if t not in type_count:
            type_count[t] = 1
        else:
            type_count[t] += 1

    return type_count


def get_unique_5cardhands(combolist):
    """
    Filters out all the hands that have the same value so we can see how many unique values
    there are.
    """
    hands = {}

    # Run through all combinations of 5 card hands
    for c in combolist:
        #  h = hand.Hand(c)
        v = evaluator.get_value(c)
        #  hands[h.value()] = h
        hands[v] = c

    return len(hands)


def sort_handslist(handdict):
    """
    Takes a list of Hands and returns a list sorted by value.
    """
    sortedhands = []
    for h in handdict:
        sortedhands.append((handdict[h].value(), handdict[h].rank(), handdict[h].cards))

    return sorted(sortedhands)


def print_unique_5cardhands(handlist):
    for h in handlist:
        print('{:<15}{:<15}{:<15}'.format(
            h[0], h[1], evaluator.print_cardlist(h[2])))


def count_all_handtypes(combolist):
    print('')
    print('Counting all the hand types in the list of {} hands.'.format(len(combosof5)))
    type_count = typecount_dict(combosof5)

    print('Results:')
    for t in type_count:
        print('{}: {}'.format(t, type_count[t]))


def enumerate_unique_5cardhands(combolist):
    print('Enumerating unique 5-card hands by value')
    unique_hands = get_unique_5cardhands(combolist)
    sortedhands = sort_handslist(unique_hands)
    print_unique_5cardhands(sortedhands)


def write_handcombos():
    print('Enumerating unique 5-card hands by value')
    unique_hands = get_unique_5cardhands()

    with open('handcombos.dat', 'wb') as db:
        pickle.dump(unique_hands, db)

if __name__ == "__main__":
    d = deck.Deck()

    print('Counting all 5 card hands in a deck')
    combosof5 = get_combolist(d.cards, 5)
    print('Combos counted.')
    print('There are {} combos of 5 in a standard deck.'.format(len(combosof5)))

    # Reuse the combolist

    count_all_handtypes(combosof5)

    enumerate_unique_5cardhands(combosof5)
