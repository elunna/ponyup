import random
from ponyup import games
from ponyup import stacks
from ponyup import logger
from ponyup import options
from ponyup import poker

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
_logger = logger.get_logger(__name__)


class Session():
    def __init__(self, gametype):
        """
        Initialize the poker Session settings.
        """
        self.gametype = gametype
        self.streets = games.GAMES[gametype]
        self.blinds = None
        self.table = None

        self.rounds = 1
        self.options = options.OPTIONS
        self.playerpool = None

    def __str__(self):
        """
        Return info about the current Session.
        """
        _str = '{} -- {} {}\n'.format(self.table.name, self.blinds.stakes(), self.gametype)
        _str += 'Round: {}\n'.format(self.rounds)
        return _str

    def new_round(self):
        _logger.debug('Created a new Round from this Session.')
        r = poker.Round(self)
        return r

    def play(self):
        """
        Defines the structure of how a single hand in the poker game is played.
        """
        print('Stub play function')

    def find_hero(self):
        _logger.debug('Attempting to find the hero player in the Session\'s table.')
        for s in self.table:
            if s.player.is_human():
                _logger.debug('Found the hero player: Seat {}, name: {}'.format(s.NUM, s.player))
                return s

    def clear_broke_players(self):
        """
        Remove all the seats that have 0 chips. Return a string showing what happened.
        """
        _logger.debug('Finding all broke players.')
        broke_players = self.table.get_broke_players()
        _str = ''
        _logger.debug('Clearing all broke players from the Session Table.')
        for seat in broke_players:
            _logger.debug('Seat {} is broke.'.format(seat.NUM))
            _str += '{} left the table with no money!\n'.format(seat.player)
            _logger.debug('Making seat {} stand up from the table.'.format(seat.NUM))
            seat.standup()
        return _str

    def table_maintainance(self):
        _logger.debug('Performing table maintenance.')
        _logger.debug('Removing broke players.')
        print(self.clear_broke_players())

        _logger.debug('Checking if we need to repopulate players to the table..')
        if self.repopulate():
            return
        else:
            _logger.debug('Checking if players are randomly leaving.')
            self.yank_from_table()

    def repopulate(self):
        """
        If there are free seats, we'll take a random chance that a new player will occupy a
        seat. If there is only one player at the table (ie: probably the human), then we MUST
        add a new player to play. Otherwise, the chance a new player will arrive will be rather
        low, ~5-10%, to give some variety in the game play.
        """
        _logger.debug('Checking how many free seats there are.')
        freeseats = self.table.get_free_seats()
        _logger.debug('Checking if only one player is at the table.')
        loneplayer = (len(self.table) - len(freeseats)) == 1

        if not freeseats:
            _logger.debug('The table is full.')
            return False

        _logger.debug('Randomizing if we\'ll have a new player enter the game.')
        freshmeat = random.randint(1, 100) <= ENTER_CHANCE

        if loneplayer or freshmeat:
            _logger.debug('A new player is needed.')
            _logger.debug('Taking a player from the player pool.')
            newplayer = self.yank_from_pool()
            _logger.debug('Randomizing which free seat the new player will occupy')
            newseat = random.choice(freeseats)
            print('{} has entered the game and taken seat {}.'.format(newplayer.name, newseat.NUM))

            _logger.debug('Seating the new player at seat {}'.format(newseat.NUM))
            newseat.sitdown(newplayer)
            _logger.debug('Calculating a random buyin.')
            buyin = stacks.random_stack(self.blinds.SMBET)
            _logger.debug('Buying the new player {} chips'.format(buyin))
            newseat.buy_chips(buyin)
        return True

    def yank_from_table(self):
        """
        Makes a random player (not including the hero) standup and leave the table.
        """
        # If there are only 2 players, ignore this.
        if len(self.table.get_players()) == 2:
            _logger.debug('There are only 2 players at the table, cannot make any randomly leave.')
            return False

        _logger.debug('Calculating if we will have a player leave the table.')
        runaway = random.randint(1, 100) <= LEAVE_CHANCE
        if runaway:
            _logger.debug('A player will be leaving.')

            _logger.debug('Starting a loop to choose the leaver.')
            while True:
                _logger.debug('Randomly choose a player to leave.')
                s = random.choice(self.table.get_players())
                if s.player.is_human():
                    _logger.debug('Seat chosen in the human hero - ignoring.')
                    # This is the human hero player - don't remove.
                    continue
                else:
                    _logger.debug('Found a CPU to make leave: seat {}'.format(s.NUM))
                    print('{} has left the table..'.format(s.player))
                    # Make the random player leave
                    _logger.debug('Making seat {} stand up from the table'.format(s.NUM))
                    s.standup()
                    return True

    def return_to_pool(self, player):
        _logger.debug('Returning player {} to the player pool'.format(player))
        self.playerpool.append(player)

    def yank_from_pool(self):
        _logger.debug('Finding a player to yank from the player pool.')
        if len(self.playerpool) == 0:
            _logger.debug('The player pool is empty.')
            return False
        else:
            _logger.debug('Choosing a random player from the player pool.')
            p = random.choice(self.playerpool)
            _logger.debug('Removing them from the player pool.')
            self.playerpool.remove(p)
            _logger.debug('Return the picked player.')
            return p
