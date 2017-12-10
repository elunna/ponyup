from . import forcedbet
from . import numtools


class Blinds(forcedbet.ForcedBet):
    def __init__(self, bb, sb, antes=0):
        """ Initialize the Blinds object with the small blind, big blind, and antes amounts.  """
        forcedbet.ForcedBet.__init__(self, bb, sb, antes)

    def __str__(self):
        """Returns the blind and ante amounts. """
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
