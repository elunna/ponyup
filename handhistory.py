import console
import datetime
import random

"""
Hand history logger. Logs the actions that take place during a round of poker.

For a normal hand history file, we will start with a header:
        * PonyupPoker Poker Game
        * Game ID#
        * Table name,
        * stakes,
        * Game type
        * time,
        * date
        * Seats, names, stack sizes

Full Tilt Poker Game #108180711: Table Pilot - $1/$2 - Limit Hold'em - 12:11:53 ET - 2009/02/24
"""

FILE = 'log.log'


class HandHistory():
    def __init__(self, _round):
        self.r = _round
        self.text = ''
        self.write_header()
        self.write_player_list()
        self.button()

    def write_header(self):
        gameid = random.randint(100000000, 999999999)
        tablename = 'twilicane'
        dt = datetime.datetime
        date = dt.today()
        time = dt.now()
        header = 'PonyUp Poker Game ID# {}: Table {} - {} - {} - {}\n'.format(
            gameid, tablename, self.r.blinds.stakes(), self.r.gametype, time, date)
        self.text += header

    def button(self):
        self.text += 'Seat {} has the button.\n'.format(self.r._table.TOKENS['D'])

    def holecards(self):
        self.text += self.r.decorate('HOLE CARDS')
        hero = self.r._table.seats[0].player
        cards = self.r._table.seats[0].hand
        self.text += 'Dealt to {}: [{}]'.format(hero, cards)

    def write_player_list(self):
        self.text += console.player_listing(self.r._table)

    def write_tokens(self):
        # Note who has the button, SB, BB, bringin, etc.
        pass

    def log(self, text):
        self.text += text + '\n'

    def write_to_file(self):
        with open(FILE, 'a') as f:
            for l in self.text:
                f.write(l)
