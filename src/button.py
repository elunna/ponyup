import random
from . import tokens
from . import dealer

""" The Button module manages the movement of the Dealer Button.
"""


class Button(tokens.Token):
    def __init__(self, table):
        tokens.Token.__init__(self, name="Button", table=table)
        self.seat = -1  # Start at -1  or None?

    def move(self):
        """ Move the button clockwise to the next valid player/seat. """
        self.seat = dealer.next_player(self.table, from_seat=self.seat)

    def randomize(self):
        """ Places the button at a random player's seat.
            If there is no players at the table, sets seat to -1.
        """
        seats = list(dealer.get_playerdict(self.table).keys())
        if len(seats) == 0:
            raise Exception('Cannot place the button, no players at table!')
        choice = random.choice(seats)
        self.seat = choice
