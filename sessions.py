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

ENTER_CHANCE = 10.0     # as a percent
LEAVE_CHANCE = 2.0      # as a percent
REBUY_CHANCE = 50.0     # as a percent


class Session():
    def __init__(self, gametype, table, blinds, playerpool=None):
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
        self.playerpool = playerpool

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

    def table_maintainance(self):
        print(self.clear_broke_players())
        if self.repopulate():
            return
        else:
            self.yank_from_table()

    def repopulate(self):
        """
        If there are free seats, we'll take a random chance that a new player will occupy a
        seat. If there is only one player at the table (ie: probably the human), then we MUST
        add a new player to play. Otherwise, the chance a new player will arrive will be rather
        low, ~5-10%, to give some variety in the game play.
        """
        freeseats = self._table.get_free_seats()
        loneplayer = (len(self._table) - len(freeseats)) == 1

        if not freeseats:
            return False

        freshmeat = random.randint(1, 100) <= ENTER_CHANCE

        if loneplayer or freshmeat:
            newplayer = self.yank_from_pool()
            newseat = random.choice(freeseats)
            print('{} has entered the game and taken seat {}.'.format(
                newplayer.name, newseat.NUM))
            newseat.sitdown(newplayer)
        return True

    def yank_from_table(self):
        """
        Makes a random player (not including the hero) standup and leave the table.
        """
        # If there are only 2 players, ignore this.
        if len(self._table.get_players()) == 2:
            return False
        runaway = random.randint(1, 100) <= LEAVE_CHANCE
        if runaway:
            while True:
                s = random.choice(self._table.get_players())
                if s.player.is_human():
                    # This is the human hero player - don't remove.
                    continue
                else:
                    # Make the random player leave
                    s.standup()
                    return True

    def return_to_pool(self, player):
        self.playerpool.append(player)

    def yank_from_pool(self):
        if len(self.playerpool) == 0:
            return False
        else:
            p = random.choice(self.playerpool)
            self.playerpool.remove(p)
            return p
