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
import datetime
LOGDIR = 'logs/'


class HandHistory(object):
    """ Keeps track of writing the details of each round of poker to a file """
    def __init__(self, _round):
        self.dt = datetime.datetime
        self.r = _round
        self.filename = self.generate_filename()
        self.text = ''
        self.write_header()
        self.write_player_list()

    def generate_filename(self):
        """ Creates a unique filename that describes the handhistory for the session, """
        stakes = '${}-${}'.format(self.r.blinds.SMBET, self.r.blinds.SMBET * 2)
        filename = 'HH_{}_-_{}_{}_{}(Pony Bits)'.format(
            self.dt.now().strftime('%Y%m%d'),
            self.r.table.name,
            self.r.gametype,
            stakes
        )
        return LOGDIR + filename

    def write_header(self):
        """ Creates a header for each new round of poker """
        date = self.dt.today()
        time = self.dt.now().strftime('%Y-%m-%d %H:%M:%S')
        header = 'PonyUp Poker Game ID# {}: Table {} - {} - {} - {}\n'.format(
            self.r.gameid,
            self.r.table.name,
            self.r.blinds.stakes(),
            self.r.gametype,
            time,
            date)
        self.log(header)

    def button(self):
        """ Writes what seat currently has the button at the start of the round. """
        self.log('Seat {} has the button.\n'.format(self.r.table.TOKENS['D']))

    def write_player_list(self):
        """ Writes what players are at the table and what stack sizes they possess. """
        self.log(self.r.table.player_listing())

    def log(self, text):
        with open(self.filename, 'a') as f:
            f.write(text + '\n')


def decorate(text):
    return '\n~~/) ' + text + ' (\~~'
    # /)(\ (\/)
    #  self.text += '~~(\ ' + text + ' /)~~'
