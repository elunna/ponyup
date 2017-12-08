from . import forcedbet
from . import numtools


class Antes(forcedbet.ForcedBet):
    def __init__(self, antes, bringin):
        forcedbet.ForcedBet.__init__(self, bb=bringin, antes=antes)
        self.bringin = bringin

    def __str__(self):
        """
        Returns the stakes, as in the small bet/big bet amounts.
        Note: For ante/bringin games, the small-bet is SB and the big-bet is BB.
        """
        _str = ''
        _str += 'Ante: ${}, '.format(numtools.fmtnum(self.antes))
        _str += 'Bringin: ${}\n'.format(numtools.fmtnum(self.bringin))
        # if sb != bb:
            # _str += 'SB: ${}, BB: ${}\n'.format(numtools.fmtnum(self.SB), numtools.fmtnum(self.BB))
        return _str

    # Set bringin?
