"""
  " The Player class manages each Players account and status. Things like name,
  " password, money available, etc.
  """

from . import names

TYPES = ['FISH', 'JACKAL', 'MOUSE', 'LION']
DATADIR = 'data/'
HUMAN_BANK_BITS = 1000


class Player(object):
    """ Defines a Player object. """
    def __init__(self, name, bank=0, playertype=None):
        if names.is_validname(name):
            self.name = name
        else:
            raise ValueError('Invalid username "{}" for object!'.format(name))

        self.bank = bank
        self.playertype = playertype

        self.strategies = None

    def __str__(self):
        """ Returns the player's name. """
        return '{}'.format(self.name)

    def __repr__(self):
        """ Same as str, returns name. """
        return str(self)

    def set_name(self, name):
        """ Checks the player name, and sets it if valid. Raises an exception if
            not valid.
        """

    def withdraw(self, amt):
        """ Removes the amount given from the player's stack and returns it. If
            the amount is more than the player has, then the remaining amount in
            the player's stack is remoevd and returned.
        """
        if amt < 0:
            raise ValueError('Player cannot bet a negative amount!')
        if amt > self.bank:
            # Put the player all-in
            amt = self.bank
            self.bank = 0
            return amt
        else:
            self.bank -= amt
            return amt

    def deposit(self, amt):
        """ Adds the specified amount of chips to the player's stack. """
        if amt < 0:
            raise Exception('Cannot add negative chips!')
        else:
            self.bank += amt

    def is_human(self):
        """ Returns True if the player is a HUMAN type, False otherwise. """
        return self.playertype == 'HUMAN'

    @property
    def bank(self):
        # return '${:.2f}'.format(self.bank)
        return round(self.__bank, 2)

    @bank.setter
    def bank(self, x):
        self.__bank = x
