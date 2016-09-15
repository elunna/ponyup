import games
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


class Session():
    def __init__(self, gametype, table, blinds, hero=None, label=None):
        """
        Initialize the poker Session settings.
        """
        self.gametype = gametype
        self.label = label
        self.rounds = 1
        self._table = table
        self.streets = games.GAMES[gametype]
        self.blinds = blinds
        self.options = options.OPTIONS
        self.hero = self.find_hero()

    def __str__(self):
        """
        Return info about the current Session.
        """
        _str = '~~~ Info about the current session: ~~~\n'
        _str += 'Game: {}\n'.format(self.gametype)
        _str += 'Stakes: {}\n'.format(self.blinds)
        _str += 'Table name: {}\n'.format(self.label)
        _str += 'Rounds played: {}\n'.format(self.rounds)
        _str += 'Hero: {}\n'.format(self.hero)
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

    def clear_broke_players(self):
        """
        Remove all the seats that have 0 chips. Return a string showing what happened.
        """
        broke_players = self._table.get_broke_players()
        _str = ''
        for seat in broke_players:
            seat.standup()
            _str += '{} left the table with no money!\n'.format(seat.player)
        return _str
