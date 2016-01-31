#!/usr/bin/env python3

import deck
import random
#  import combotests
import pickle
#  import evaluator
import hand


def copy_list(listx):
    newlist = []
    for i in listx:
        newlist.append(i)
    return newlist

if __name__ == "__main__":
    print('SIMULATION:')
    print('Test the winrates of all 5 card poker hands.')
    REPS = 1000000
    print('Run {} trials for each unique hand.'.format(REPS))
    print('*'*80)

    print('')
    #  print('Creating the hand combos')
    print('Importing the hand combos')

    with open('handcombos.dat', 'rb') as db:
        hands = pickle.load(db)

    print('db length = {}'.format(len(hands)))

    #  r = hands.popitem()
    hero = hand.Hand(random.choice(hands)[2])

    #  print('random hand = {}'.format(evaluator.print_cardlist(hero[2])))
    print('random hand = {}'.format(hero.display()))
    #  print('rank: {}'.format(hero[1]))
    print('rank: {}'.format(hero.handrank))
    print('value: {}'.format(hero.value))

    d = deck.Deck()
    print('Removing cards in the hand from the deck')
    for h in hero.cards:
        d.cards.remove(h)
        #  print(h in d.cards)
    print('modified deck size: {}'.format(len(d)))

    TRIALS = 10000
    WINS = 0
    # Begin trials

    for i in range(TRIALS):
        deck_copy = deck.Deck(copy_list(d.cards))
        deck_copy.shuffle()
        villain = hand.Hand([deck_copy.deal() for x in range(5)])
        if hero.value > villain.value:
            WINS += 1

    print('='*80)
    print('Performs {} trials'.format(TRIALS))
    print('Hero won {} times.'.format(WINS))
    WIN_PERCENT = WINS / TRIALS
    print('Win percent: %{}'.format(WIN_PERCENT * 100))
