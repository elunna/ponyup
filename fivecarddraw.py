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
    keep = []
    discard = []
    print('')
    #  print('Rank = {}'.format(ranks))
    for c in hand:
        #  if c.rank == str(ranks):
        if c.rank in ranks:
            keep.append(c)
        else:
            discard.append(c)
    # Return both the remainder and the discards
    return keep, discard


def pop_suits(hand, suit):
    # Remove ALL BUT the suit given.
    keep = []
    discard = []
    print('')
    #  print('Suit = {}'.format(suit))
    for c in hand:
        if c.suit == suit:
            keep.append(c)
        else:
            discard.append(c)
    # Return both the remainder and the discards
    return keep, discard


def auto_discard(hand):
    # hand is a Hand object
    DIS_RANKS = ['PAIR', 'THREE OF A KIND', 'FOUR OF A KIND']
    discard = []
    #  discard = None

    h = evaluator.sort_ranks(hand.cards)

    if hand.handrank == 'HIGH CARD':
        # Draws
        copy = sorted(hand.cards[:])

        # Test for flush draw
        maxsuit, qty = evaluator.get_longest_suit(copy)
        if qty == 4:
            print('Found a flush draw! for {}'.format(maxsuit))
            keep, discard = pop_suits(copy, maxsuit)

        # Test for open-ended straight draw(s)
        elif evaluator.get_connectedness(copy[0:4]) == 0:
            keep = copy[0:4]
        elif evaluator.get_connectedness(copy[1:5]) == 0:
            keep = copy[1:5]

        # Test for gutshot straight draw(s)
        elif evaluator.get_connectedness(copy[0:4]) == 1:
            keep = copy[0:4]
        elif evaluator.get_connectedness(copy[1:5]) == 1:
            keep = copy[1:5]
        else:
            highcards = h[0][1]
            keep, discard = pop_ranks(hand.cards, highcards)

        if len(discard) == 0:
            print('straight draw?')
            for c in hand.cards:
                if c not in keep:
                    discard.append(c)

    elif hand.handrank in DIS_RANKS:
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
    h = hand.Hand(r)
    #  print('Creating a hand...: {}'.format(h))
    #  print(h)
    print('Value: {:<15} Rank: {:<15}'.format(h.value, h.handrank))
    #  print('Rank: {}'.format(h.handrank))

    #  print('auto_discard()')
    k, d = auto_discard(h)

    print('Keep: {}'.format(evaluator.print_cardlist(k)))
    print('Discard: {}'.format(evaluator.print_cardlist(d)))


if __name__ == "__main__":
    test()
