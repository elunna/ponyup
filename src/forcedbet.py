"""
  " Tools for managing poker blind structures.
  """
from abc import ABCMeta
from abc import abstractmethod
from . import numtools


class ForcedBet(object):
    """ Manages a forced bet structure on a table. """
    __metaclass__ = ABCMeta

    def __init__(self, bb, sb=0, antes=0):
        self.sb = sb
        self.bb = bb
        self.antes = antes

    @abstractmethod
    def __str__(self):
        return 'ForcedBet object! {}-{}'.format(self.antes, self.bb)

    def stakes(self):
        """
        Returns the stakes, as in the small bet/big bet amounts. For games that only use blinds
        (without antes), we calculate the amounts by using the Big Blind as the small bet, and
        twice the Big Blind as the big bet.
        """
        return '${}-${}'.format(self.bb, self.bb * 2)

    def big_blinds(self, stack):
        """ Returns how many big blinds are in the stack. Uses the Big Blind from
            the current level and rounds down.
        """
        return numtools.round_number(stack / self.bb)

    def trueBB(self, players):
        """ Calculates the effective BB given how many players are at the table.
            When antes come into play it changes how much each hand costs.
        """
        if self.antes == 0:
            return self.bb
        pot = self.sb + self.bb + (players * self.antes)
        return round(pot * .66)

    def effectiveBB(self, stack, players):
        """ Returns how many big blinds are effectively in the stack. First adds
            up the current pot which is (SB + BB + Antes). The players variable
            is an integer which specified how many antes to add. Then the
            effective big blind is 2/3rds of the pot. Returns a rounded integer.
        """
        return numtools.round_number(stack / self.trueBB(players))
