"""
  " Seats manage Players, chip stack, and Hands.
  " Note: Maybe repr should return the position of the seat?"
  """

from . import hand


class Seat(object):
    """ Defines a Seat object that occupies a Table.  """
    def __init__(self, table=None, position=0):
        self.table = table
        self.position = position  # Seat number at the table, after the dealer.
        self.player = None
        self.hand = hand.Hand()
        self.stack = 0

    def __str__(self):
        if self.player is None:
            return 'Open Seat'
        else:
            return str(self.player)

    def sitdown(self, player):
        """ Takes a Player and sets them in this seat if not occupied. """
        if not self.vacant():
            raise Exception('The seat is currently occupied!')
        else:
            self.player = player
            self.hand = hand.Hand()

    def standup(self):
        """ Removes the Player from this seat and refunds their money. """
        self.player.deposit(self.stack)
        self.stack = 0
        p = self.player
        self.player = None
        self.hand = hand.Hand()
        return p

    def vacant(self):
        return self.player is None

    def occupied(self):
        return self.player is not None

    def has_hand(self):
        """ Returns True if the player at this seat currently has a Hand, False otherwise """
        return len(self.hand) > 0

    def has_chips(self):
        return self.stack > 0

    def buy_chips(self, amount):
        if self.player is None:
            raise ValueError('No player is sitting to buy chips!')
        elif amount > self.player.bank:
            raise ValueError('Player cannot buy more chips than they can afford!')

        self.stack += self.player.withdraw(amount)

    def win(self, amount):
        """ Award the given amount of chips to the current players stack. """
        if amount <= 0:
            raise ValueError('Amount won needs to be greater than 0!')
        self.stack += amount

    def bet(self, amt):
        """ Removes the given amount from the players stack and returns it. """
        if amt > self.stack:
            amt = self.stack
        elif amt <= 0:
            raise ValueError('Amount bet needs to be greater than 0!')

        self.stack -= amt
        return amt

    def fold(self):
        """ Removes all the cards in the hand and returns them as a list.
        """
        copy = self.hand.cards[:]
        self.hand.cards = hand.Hand()
        return copy
