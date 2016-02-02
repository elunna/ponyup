#!/usr/bin/env python3

import gametools
import deck
import handtests
import evaluator
import hand
#  import table
#  import player


class Round():
    def __init__(self, game):
        self.game = game
        self.street = 0
        self.pot = 0
        self.d = deck.Deck()
        self.players = self.game.table.get_players()

    def play(self):
        # Advance round counter

        # Get activeplayers
        for p in self.players:
            for c in range(5):
                p.hand.add(self.d.deal())

        # Remember starting stacks of all playerso
        #  self.startingstacks = []

        # Postblinds

        # Deal cards

        # Pre-draw betting round

        # Check for winners

        # Discard/redraw phase

        # Post-draw betting round

        # Check for winners/showdown
        gametools.get_winner(self.players)

        # Award pot

        # Move the table button
        pass


def pop_ranks(hand, ranks):
    # Remove ALL BUT the rank given.
    discard = []
    keep = []
    print('')
    print('Rank = {}'.format(ranks))
    for c in hand:
        #  if c.rank == str(ranks):
        if c.rank in ranks:
            keep.append(c)
        else:
            discard.append(c)
    # Return both the remainder and the discards
    return keep, discard


def auto_discard(hand):
    # hand is a Hand object
    DIS_RANKS = ['HIGH CARD', 'PAIR', 'THREE OF A KIND', 'FOUR OF A KIND']

    h = evaluator.sort_ranks(hand.cards)

    # Draws
    # Test for straight/flush draw
    # Test for flush draw
    #  if evaluator.count_suited(hand) == 4:
        # Figure out what the suit it
    # Test for straight draw(s)

    if hand.handrank in DIS_RANKS:
        print('Performing standard discard')
        highcards = h[0][1]
        keep, discard = pop_ranks(hand.cards, highcards)

    elif hand.handrank == 'TWO PAIR':
        print('Performing two-pair discard')
        # Keep the twp pair, discard 1.
        highcards = h[0][1] + h[1][1]

        keep, discard = pop_ranks(hand.cards, highcards)

    # Obviously we will stand pat on:
    #   Straight, Flush, Full House, Straight/Royal Flush
    return keep, discard

def main():
    # Make hands

    _table = gametools.setup_test_table(2)
    game = gametools.Game('2/4', _table)

    r = Round(game)
    r.play()


def test():
    print('Five Card Draw tests')
    print('')
    print('*'*80)
    print('Testing discard function')
    print('')
    r = handtests.dealhand(5)
    print('Random 5 cards: {}'.format(evaluator.print_cardlist(r)))
    print('Creating a hand...')
    h = hand.Hand(r)
    print(h)
    print('Value: {}'.format(h.value))
    print('Rank: {}'.format(h.handrank))

    print('auto_discard()')
    k, d = auto_discard(h)

    print('Keep: {}'.format(evaluator.print_cardlist(k)))
    print('Discard: {}'.format(evaluator.print_cardlist(d)))


if __name__ == "__main__":
    test()
