import poker
import options
"""
The Session object manages the general structure of a poker cash game session.

It is responsible for:
    * knowing the game type,
    * the table,
    * the stakes,
    * keeping track of how many rounds have been played.
    * keeping track of how long the session has lasted.
    * keeping a handhistory log of all rounds played
    * Keeping track of when and what players get knocked out, for purposes of altering the
    blind tokens if necessary.

"""

DISPLAYWIDTH = 70
GAMES = {
    #  'OMAHA': [1, 1, 2, 2],
    #  'HOLDEM': [1, 1, 2, 2],
    'FIVE CARD DRAW': [1, 2],
    'FIVE CARD STUD': [1, 1, 2, 2],
    #  'SEVEN CARD STUD': [1, 1, 2, 2, 2],
}


class Session():
    def __init__(self, gametype, table, blinds, hero=None):
        """
        Initialize the poker Session settings.
        """
        self.gametype = gametype
        self.rounds = 1
        self._table = table
        self.streets = GAMES[gametype]
        self.blinds = blinds
        self.options = options.OPTIONS
        self.hero = self.find_hero()

    def __str__(self):
        """
        Returns the Session info.
        """
        _str = '{} {}'.format(self.blinds.stakes(), self.gametype)
        rnd_str = 'Round: {:<5}\n'.format(self.rounds)
        _str += rnd_str.rjust(DISPLAYWIDTH - len(_str))

        return _str

    def new_round(self):
        return poker.Round(self)

    def play(self):
        """
        Defines the structure of how a single hand in the poker game is played.
        """
        print('Stub play function')

    def find_hero(self):
        for s in self._table:
            if s.player.is_human():
                return s
