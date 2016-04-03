#!/usr/bin/env python3

import deck
import hand
import combos
import pokerhands
import draw5

TRIALS = 10000

# Brute Force: Basic idea
# 1) We take a drawy type hand
# 2) We take all the possible discard combos
# 3) We run each discard through XXXXX trials againts random hands
# 4) We find which discard combo has the best %

# Measured:
# 1) We take a drawy type hand
# 2) We take all the possible discard combos
# 3) Find all the complementary combos that would improve the hand
# 4) Assign a minimum threshold value for improvement
# 5) We find which discard combo has the best %


def test(cards):
    if len(cards) != 5:
        raise ValueError('Non-valid hand!')
        exit()

    d = deck.Deck()
    for c in cards:
        c.hidden = False
        # Remove cards in hand from deck
        d.remove(c)

    # Unhide cards in deck
    for c in d.cards:
        c.hidden = False

    print('Cards: {}'.format(cards))
    discard_combos = combos.get_allcombos(cards)
    print('Combos VS RANDOM HANDS!')
    print('{} Trials'.format(TRIALS))

    results = []
    for dis in discard_combos:
        wins = run_trial(d, cards[:], dis)
        print('{:20}: Discard {:15} -- Win {}'.format(str(cards), str(dis), wins))
        results.append((wins, dis))

    print('')
    print('Sorting and printing our results for {}'.format(cards))
    for r in sorted(results):
        print(r)


def run_trial(mydeck, c_copy, discard):
    # Remove the discard cards from hand
    for dis in discard:
        c_copy.remove(dis)

    WINS = 0

    # Begin trials
    for i in range(TRIALS):
        d = deck.Deck(mydeck.cards[:])
        d.shuffle()

        while len(c_copy) < 5:
            #  hero.add(d_copy.deal())
            c_copy.append(d.deal())

        hero = hand.Hand(c_copy)

        #  villain = hand.Hand([d_copy.deal() for x in range(5)])
        villain = hand.Hand()

        for v in range(5):
            villain.add(d.deal())

        # Make villain discard?
        #  villian_dis = fivecarddraw.auto_discard(villain)
        #  for c in villian_dis:
            #  villain.discard(c)
            #  villain.add(d_copy.deal())

        if len(hero) != 5:
            raise ValueError('Hero hand is corrupt!')
        if len(villain) != 5:
            raise ValueError('Villain hand is corrupt!')

        #  mucksize = len(hero) + len(villain) + len(discard) + len(villian_dis) + len(d_copy)
        mucksize = len(hero) + len(villain) + len(discard) + len(d)

        if mucksize != 52:
            print('mucksize = {}'.format(mucksize))
            print('hero hand: {}'.format(len(hero)))
            print('villain hand: {}'.format(len(villain)))
            print('hero discard: {}'.format(len(discard)))
            print(discard)
            #  print('villain discard: {}'.format(villian_dis))
            print('deck: {}'.format(sorted(d.cards)))
            print('deck size: {}'.format(len(d)))

            for i in discard:
                if i in d.cards:
                    print('{} was found in the deck - should be discard!'.format(i))

            raise ValueError('Deck miscount!')

        print('Hero: {}'.format(hero))
        print('Villain: {}'.format(villain))
        input('Press enter...')

        if hero.value > villain.value:
            WINS += 1

        exit()

    #  WIN_PERCENT = WINS / TRIALS
    #  return WIN_PERCENT
    return WINS

if __name__ == "__main__":
    print('5 Card Draw - Discard Evaluator:')
    print('Test the winrates of different discard combos.')
    print('Run {} trials for each unique hand.'.format(TRIALS))
    print('*'*80)
    h1 = pokerhands.deal_OESD()
    test(h1)
    #  h2 = handtests.deal_GSSD()
    #  test(h2)
