import games
import poker
import options
import random

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
    def __init__(self, gametype, table, blinds, hero=None):
        """
        Initialize the poker Session settings.
        """
        self.gametype = gametype
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
        _str = '{} -- {} {}\n'.format(self._table.name, self.blinds.stakes(), self.gametype)
        _str += 'Round: {}\n'.format(self.rounds)
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

    def repopulate(self):
        """
        If there are free seats, we'll take a random chance that a new player will occupy a
        seat. If there is only one player at the table (ie: probably the human), then we MUST
        add a new player to play. Otherwise, the chance a new player will arrive will be rather
        low, ~5-10%, to give some variety in the game play.
        """
        CHANCE = 10.0   # as a percent
        freeseats = self._table.get_free_seats()

        if freeseats:
            result = random.randint(1, 100)
            if result <= CHANCE:
                print('Free seat! Repopulating!')
                pass
                #  newplayer = player.factory(names.
