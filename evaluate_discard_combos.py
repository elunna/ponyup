#!/usr/bin/env python3

import deck
import hand
import combos
import pokerhands

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


def new_deck_minus_hand(_hand):
    d = deck.Deck()
    d.unhide()
    for c in _hand:
        # Remove cards in hand from deck
        d.remove(c)
    return d


def rm_discards_from_hand(cards, discards):
    # Remove the discard cards from hand
    cards = cards[:]
    for x in discards:
        cards.remove(x)
    return cards


def test(cards):
    d = new_deck_minus_hand(cards)

    print('Cards: {}'.format(cards))
    discard_combos = combos.get_allcombos(cards)

    print('All {} combos of discards...'.format(len(discard_combos)))
    for dc in discard_combos:
        print(dc)

    print('Combos VS RANDOM HANDS!')
    print('{} Trials'.format(TRIALS))

    results = []
    for dc in discard_combos:
        h = rm_discards_from_hand(cards, dc)

        wins = run_trials(d, h, dc)
        results.append((wins, dc))
        #  print('{:20}: Discard {:15} -- Win {}'.format(str(cards), str(dc), wins))
    return results


def run_trials(_deck, _hand, discard):
    WINS = 0
    # Remove discards from deck
    for c in discard:
        _deck.remove(c)

    for i in range(TRIALS):
        # Reset deck
        d = deck.Deck(_deck.cards[:])
        d.shuffle()

        # Redraw for the hand.
        while len(_hand) < 5:
            _hand.append(d.deal())

        hero = hand.Hand(_hand)

        villain = hand.Hand([d.deal() for x in range(5)])

        if len(hero) != 5 or len(villain) != 5:
            raise ValueError('Hero or villian hand is corrupt!')

        mucksize = len(hero) + len(villain) + len(discard) + len(d)

        #  if mucksize != 52:
            #  raise ValueError('Deck miscount!')

        if mucksize != 52:
            print('mucksize = {}'.format(mucksize))
            print('hero hand: {}'.format(len(hero)))
            print('villain hand: {}'.format(len(villain)))
            print('hero discard: {}'.format(len(discard)))
            print('hero discard: {}'.format(discard))
            print('deck: {}'.format(sorted(d.cards)))
            print('deck size: {}'.format(len(d)))

            playedcards = []
            playedcards.extend(hero.cards)
            playedcards.extend(villain.cards)

            for i in discard:
                if i in d.cards:
                    print('{} was found in the deck - was discarded!'.format(i))

            for i in playedcards:
                if i in d.cards:
                    print('{} was found in the deck - already played!'.format(i))

            raise ValueError('Deck miscount!')

        print('Hero: {}, Villain: {}'.format(hero, villain))
        if hero.value() > villain.value():
            WINS += 1

    return WINS

if __name__ == "__main__":
    print('5 Card Draw - Discard Evaluator:')
    print('Test the winrates of different discard combos.')
    print('Run {} trials for each unique hand.'.format(TRIALS))
    print('*'*80)
    h1 = pokerhands.make('OESD', hidden=False)
    results = test(h1)

    print('')
    for r in sorted(results):
        print(r)
