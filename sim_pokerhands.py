#!/usr/bin/env python3

import deck
#  import random
import pickle
import hand

TRIALS = 10000


def run_trial(testhand, trials):
    # Then return a list of: value/type/cards/win %

    hero = hand.Hand(testhand)
    d = deck.Deck()
    #  Removing cards in the hand from the deck
    for h in hero.cards:
        d.cards.remove(h)

    WINS = 0

    # Begin trials
    for i in range(TRIALS):
        deck_copy = deck.Deck(d.cards[:])
        deck_copy.shuffle()
        villain = hand.Hand([deck_copy.deal() for x in range(5)])
        if hero.value > villain.value:
            WINS += 1

    WIN_PERCENT = WINS / TRIALS
    print('{:<15}{:<15}{:<15}{}'.format(hero.value, hero.handrank, str(hero), WIN_PERCENT))

    return [hero.value, hero.handrank, hero, WIN_PERCENT]


def write_handtrials(results):
    print('Creating a report in handtrials.dat')

    with open('handtrials.dat', 'w') as f:
        for r in results:
            f.write('{:<15}{:<15}{:<15}{}\n'.format(r[0], r[1], str(r[2]), r[3]))


if __name__ == "__main__":
    print('SIMULATION:')
    print('Test the winrates of all 5 card poker hands.')
    print('Run {} trials for each unique hand.'.format(TRIALS))
    print('*'*80)

    print('')
    #  print('Creating the hand combos')
    print('Importing the hand combos')

    with open('handcombos.dat', 'rb') as db:
        hands = pickle.load(db)

    resultlist = []
    for h in hands:
        resultlist.append(run_trial(h[2], TRIALS))

    write_handtrials(resultlist)
