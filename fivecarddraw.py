#!/usr/bin/env python3

import gametools
import deck
#  import hand
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


def main():
    # Make hands

    _table = gametools.setup_test_table(2)
    game = gametools.Game('2/4', _table)

    r = Round(game)
    r.play()


def test():
    print('This... Is.... Five Card Draw.')
    print('')
    print('Testing a new game')
    print('Creating a 2/4 game with a 2 player table')
    print('*'*80)
    _table = gametools.setup_test_table(2)
    game = gametools.Game('2/4', _table)
    print(game)

if __name__ == "__main__":
    test()
