from . import forcedbet
from . import numtools


class Blinds(forcedbet.ForcedBet):
    def __init__(self, bb, sb, antes=0):
        """ Initialize the Blinds object with a given blind structure.  """
        forcedbet.ForcedBet.__init__(self, bb, sb, antes)

    def __str__(self):
        """
        Returns the stakes, as in the small bet/big bet amounts.
        Note: For ante/bringin games, the small-bet is SB and the big-bet is BB.
        """
        _str = ''
        if self.antes > 0:
            _str += 'Ante: ${}, '.format(numtools.fmtnum(self.antes))
        _str += 'SB: ${}, BB: ${}\n'.format(numtools.fmtnum(self.sb), numtools.fmtnum(self.bb))
        return _str

    def sb_to_ante_ratio(self):
        """ Returns the SB-to-Ante ratio of the current small blind and ante. """
        # Use only one decimal place.
        if self.antes > 0:
            return round(self.sb / self.antes, 1)
        else:
            return 0

    def set_blinds(self, table):
        if len(table.get_players()) == 2:
            table.TOKENS['SB'] = table.TOKENS['D']
            table.TOKENS['BB'] = table.next_player(table.TOKENS['D'])
        elif len(table.get_players()) > 2:
            table.TOKENS['SB'] = table.next_player(table.TOKENS['D'])
            table.TOKENS['BB'] = table.next_player(table.TOKENS['SB'])
        else:
            raise ValueError('Not enough players at the table!')
