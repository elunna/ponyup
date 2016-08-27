#!/usr/bin/env python3
import game
import setup_table

STARTINGCHIPS = 1000


class Session():
    """
    The Game object manages the general structure of a poker game. It sets up the essentials:
        game type, the table, and stakes.  The play() method defines the structure of how a
        single hand in the poker game is played.
    """
    def __init__(self, gametype, structure, tablesize=6, hero=None):
        """
        Initialize the poker Game.
        """
        self.blinds = structure
        self.rounds = 1
        self._table = setup_table.make(tablesize, hero)
        self._table.randomize_button()

        for p in self._table:
            p.chips = STARTINGCHIPS

    def __str__(self):
        """
        Represents the game as the round # and the stakes level.
        """
        _str = 'Round: {:<5} '.format(self.rounds)
        _str += 'Stakes: {}'.format(self.blinds.__str__().rjust(36))

        return _str

    def play(self):
        print('Stub play function')
