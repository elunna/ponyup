#!/usr/bin/env python3

from __future__ import print_function
import deck
import hand
import evaluator
import shelve
import pickle


def count_all_handtypes(handlist):
    print('#'*80)
    print('')
    print('Counting the hand types in all 5 card combos')

    type_count = {}

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
    for c in evaluator.get_combos(d.cards, 5):
        h = hand.Hand(c)
        hands[h.value] = h

    print('')
    print('Number of unique hands: {}'.format(len(hands)))

    return hands


def sorted_hands_list(handdict):
    # Sort by value
    sortedhands = []
    for h in handdict:
        #  sortedhands.append(tuple(hands[h].value, hands[h].handrank, str(hands[h])))
        #  print('{:<10}{:<15}{:<15}'.format(hands[h].value, hands[h].handrank, str(hands[h]) ))
        sortedhands.append((handdict[h].value, handdict[h].handrank, handdict[h].cards))

    return sorted(sortedhands)


def print_unique_5cardhands(handlist):
    for h in handlist:
        #  sortedhands.append(tuple(hands[h].value, hands[h].handrank, str(hands[h])))
        print('{:<15}{:<15}{:<15}'.format(
            h[0], h[1], h[2]))


def print_holdem_startinghands():
    for c in list(evaluator.get_combos(d.cards, 2)):
        #  print(evaluator.print_cardlist('[{}] ]'.format(c)), end='')
        print('[{}] '.format(evaluator.print_cardlist(c)))


# !!! Not working yet....
def write_handcombos2(hands):
    with open('handcombos.dat', 'wb') as db:
        pickle.dump(hands, db)


if __name__ == "__main__":
    print('#'*80)
    print('')
    print('Combo tests')

    d = deck.Deck()

    combosof1 = list(evaluator.get_combos(d.cards, 1))
    print('Combos of 1 total: {}'.format(len(combosof1)))

    combosof2 = list(evaluator.get_combos(d.cards, 2))
    #  combosof2 = list(evaluator.get_combos(d.cards, 2))
    # Verified there should be 1326 2 card combos
    print('Combos of 2 total: {}'.format(len(combosof2)))

    combosof3 = list(evaluator.get_combos(d.cards, 3))
    # Verified there should be 22100 2 card combos
    print('Combos of 3 total: {}'.format(len(combosof3)))

    combosof4 = list(evaluator.get_combos(d.cards, 4))
    # Not verified yet.
    print('Combos of 4 total: {}'.format(len(combosof4)))

    combosof5 = list(evaluator.get_combos(d.cards, 5))
    # Verified there should be 25989602 card combos
    print('Combos of 5 total: {}'.format(len(combosof5)))

    # Warning, takes a while!
    # 01/25/16: Verified that the counts are all exactly correct.
    #  print('*'*80)
    #  print('Counting all 5 card hands in a deck')
    #  count_all_handtypes(combosof5)

    print('*'*80)
    print('Enumerating unique 5-card hands by value')
    unique_hands = get_unique_5cardhands()
    #  write_handcombos(fivecarddict)
    write_handcombos2(sorted_hands_list(unique_hands))

    #  sortedhands = sorted_uniquehands_list(fivecarddict)

    #  print_unique_5cardhands(sortedhands)

    #  print('*'*80)
    #  print('Display all holdem starting hands.')
    #  print_holdem_startinghands()
