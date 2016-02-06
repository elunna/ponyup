#!/usr/bin/env python3

import gametools
import deck
import handtests
import evaluator as ev
import hand
import card
#  import sys
#  import table
import player


class Round():
    def __init__(self, game):
        self.game = game
        self.street = 0
        self.pot = 0
        self.d = deck.Deck()
        # Get activeplayers
        self.players = self.game.table.get_players()
        self.muck = deck.Deck([])

    def play(self):
        self.d.shuffle()
        self.d.shuffle()
        self.d.shuffle()

        # Advance round counter
        self.game.rounds += 1

        # Check that no players have lingering cards
        #  print('displaying hand lengths')
        #  for p in self.players:
            #  print(len(p._hand))
            #  if p is not None:
                #  if len(p._hand) > 0:
                    #  raise ValueError('Player has cards when they should not!')

        # Remember starting stacks of all playerso
        #  self.startingstacks = []

        # Postblinds

        # Deal cards
        for i in range(5):
            self.players[0].add(self.d.deal())
            self.players[1].add(self.d.deal())

        # Pre-draw betting round
        # Show table post draw
        print(self.game.table)

        # Check for winners
        #  print('Seat 1: {}'.format(self.players[0]._hand))
        #  print('Seat 2: {}'.format(self.players[1]._hand))

        # Discard/redraw phase
        d1 = auto_discard(self.players[0]._hand)
        print('{} discards {}'.format(self.players[0], d1))

        d2 = auto_discard(self.players[1]._hand)
        print('{} discards {}'.format(self.players[1], d2))
        print('')

        for c in d1:
            self.players[0].discard(c)
            self.players[0].add(self.d.deal())

        for c in d2:
            self.players[1].discard(c)
            self.players[1].add(self.d.deal())

        # Show table post draw
        print(self.game.table)

        # Post-draw betting round

        # Check for winners/showdown
        gametools.get_winner(self.players)

        # Award pot

        # Clear hands
        for p in self.players:
            p.fold()
        # Move the table button
        self.game.table.move_button()


def auto_discard(hand):
    # hand is a Hand object

    # Obviously we will stand pat on:
    PAT_HANDS = ['STRAIGHT', 'FLUSH', 'FULL HOUSE', 'STRAIGHT FLUSH', 'ROYAL FLUSH']
    DIS_RANKS = ['PAIR', 'THREE OF A KIND', 'FOUR OF A KIND']
    discard = []

    h = ev.sort_ranks(hand.cards)

    if hand.handrank in PAT_HANDS:
        #  keep = hand.cards
        pass
    elif hand.handrank in DIS_RANKS:
        #  standard discard
        highcards = h[0][1]
        discard = ev.pop_ranks(hand.cards, highcards)
    elif hand.handrank == 'TWO PAIR':
        #  print('Performing two-pair discard')
        # Keep the twp pair, discard 1.
        highcards = h[0][1] + h[1][1]

        discard = ev.pop_ranks(hand.cards, highcards)

    elif hand.handrank == 'HIGH CARD':
        # Draws
        copy = sorted(hand.cards[:])

        # Test for flush draw
        maxsuit, qty = ev.get_longest_suit(copy)

        if qty == 4:
            #  print('Found a flush draw! for {}'.format(maxsuit))
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
    print('FIVE CARD DRAW!')
    print('Initializing new game...\n')

    hero = player.Player('Hero')
    _table = gametools.setup_test_table(2)
    _table.remove_player(0)
    _table.add_player(0, hero)

    game = gametools.Game('2/4', _table)

    print('Randomizing the button position.')
    _table.randomize_button()

    playing = True

    while playing:
        print('*'*80)
        print(game)
        #  print(_table)
        newround = Round(game)
        newround.play()
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
    print('Random 5 cards: {}'.format(ev.print_cardlist(r)))
    h = hand.Hand(r)
    #  print('Creating a hand...: {}'.format(h))
    #  print(h)
    print('Value: {:<15} Rank: {:<15}'.format(h.value, h.handrank))
    #  print('Rank: {}'.format(h.handrank))

    #  print('auto_discard()')
    d = auto_discard(h)

    #  print('Keep: {}'.format(k))
    print('Discard: {}'.format(d))


if __name__ == "__main__":
    #  main()
    test()
