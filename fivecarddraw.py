#!/usr/bin/env python3

import gametools
#  import deck
import handtests
import evaluator as ev
import hand
import card
import os
import player
import game


def is_integer(num):
    """ Determines if the variable is an integer"""
    try:
        int(num)
        return True
    except ValueError:
        return False


def human_discard(hand):
    print('Please enter the cards you want to discard:')
    print('Example: 0 to discard the first card, 01 to discard the first 2, etc')
    for i, c in enumerate(hand.cards):
        print('#{}: {}'.format(i, c))

    choice = input(':> ')
    # Split up the #s, and reverse them so we can remove them without the list
    # collapsing and disrupting the numbering.
    choice = sorted(list(choice), reverse=True)
    discards = []
    for c in choice:
        if is_integer(c):
            discards.append(hand.cards[int(c)])
        else:
            pass
    return discards


def auto_discard(hand):
    # hand is a Hand object

    # Obviously we will stand pat on:
    PAT_HANDS = ['STRAIGHT', 'FLUSH', 'FULL HOUSE', 'STRAIGHT FLUSH', 'ROYAL FLUSH']
    DIS_RANKS = ['PAIR', 'THREE OF A KIND', 'FOUR OF A KIND']
    discard = []

    h = ev.sort_ranks(hand.cards)

    if hand.handrank in PAT_HANDS:
        pass
    elif hand.handrank in DIS_RANKS:
        #  standard discard
        highcards = h[0][1]
        discard = ev.pop_ranks(hand.cards, highcards)
    elif hand.handrank == 'TWO PAIR':
        # Keep the twp pair, discard 1.
        highcards = h[0][1] + h[1][1]

        discard = ev.pop_ranks(hand.cards, highcards)

    elif hand.handrank == 'HIGH CARD':
        # Draws
        copy = sorted(hand.cards[:])

        # Test for flush draw
        maxsuit, qty = ev.get_longest_suit(copy)

        if qty == 4:
            discard = ev.pop_suits(copy, maxsuit)

        # Test for open-ended straight draw(s)
        elif ev.get_allgaps(copy[0:4]) == 0:
            keep = copy[0:4]
        elif ev.get_allgaps(copy[1:5]) == 0:
            keep = copy[1:5]

        # Test for gutshot straight draw(s)
        elif ev.get_allgaps(copy[0:4]) == 1:
            keep = copy[0:4]
        elif ev.get_allgaps(copy[1:5]) == 1:
            keep = copy[1:5]

        # Draw to high cards
        elif card.VALUES[h[2][1]] > 9:
            highcards = h[0][1] + h[1][1] + h[2][1]
            discard = ev.pop_ranks(hand.cards, highcards)
        elif card.VALUES[h[1][1]] > 9:
            highcards = h[0][1] + h[1][1]
            discard = ev.pop_ranks(hand.cards, highcards)

        elif qty == 3:
            # Backdoor flush draw
            discard = ev.pop_suits(copy, maxsuit)

        # Draw to an Ace almost as a last resort
        elif h[1][1] == 'A':
            discard = ev.pop_ranks(hand.cards, 'A')

        # Backdoor straight draws are pretty desparate
        elif ev.get_allgaps(copy[0:3]) == 0:
            keep = copy[0:3]
        elif ev.get_allgaps(copy[1:4]) == 0:
            keep = copy[1:4]
        elif ev.get_allgaps(copy[2:5]) == 0:
            keep = copy[2:5]

        # 1-gap Backdoor straight draws are truly desparate!
        elif ev.get_allgaps(copy[0:3]) == 1:
            keep = copy[0:3]
        elif ev.get_allgaps(copy[1:4]) == 1:
            keep = copy[1:4]
        elif ev.get_allgaps(copy[2:5]) == 1:
            keep = copy[2:5]
        else:
            # Last ditch - just draw to the best 2???
            highcards = h[0][1] + h[1][1]
            discard = ev.pop_ranks(hand.cards, highcards)

        if len(discard) == 0:
            for c in hand.cards:
                if c not in keep:
                    discard.append(c)

    return discard


def main():
    os.system('clear')
    print('FIVE CARD DRAW!')
    print('Initializing new game...\n')

    hero = player.Player('Hero', 'HUMAN')
    t = gametools.setup_test_table(2)
    t.remove_player(0)
    t.add_player(0, hero)

    g = game.Game('2/4', t)

    print('Randomizing the button position.')
    t.randomize_button()

    playing = True

    while playing:
        os.system('clear')
        print('*'*80)
        print(g)
        #  print(_table)
        #  newround = game.Round(g)
        # Play a round of five card draw
        #  game.playround(g)
        g.playround()
        choice = input('keep playing? >')
        if choice == 'n':
            playing = False
    exit()


def test():
    print('Five Card Draw tests')
    print('')
    print('*'*80)
    print('Testing discard function')
    print('')
    r = handtests.dealhand(5)
    print('Random 5 cards: {}'.format(r))
    h = hand.Hand(r)
    print('Value: {:<15} Rank: {:<15}'.format(h.value, h.handrank))

    d = auto_discard(h)
    print('Discard: {}'.format(d))


if __name__ == "__main__":
    main()
    #  test()
