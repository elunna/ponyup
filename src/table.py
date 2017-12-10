"""
  " The table manages Seats and the addition and removal of players..
  """

from . import seat
from . import button

VALID_SIZES = list(range(2, 10))


class Table(object):
    """ Manages a table of seats """
    def __init__(self, size):
        if size not in VALID_SIZES:
            raise ValueError('Not a valid table size!')
        self.seats = [seat.Seat(self, i) for i in range(size)]
        self.btn = button.Button(self)

    def __str__(self):
        """ Return the name of the table with some brief info."""
        # Table name, # of seats
        return 'Table: {} seats'.format(len(self.seats))

    def __len__(self):
        """ Return the total # of seats. """
        return len(self.seats)

    def __iter__(self):
        """ Creates an iterator for the table seats. Iterates over all seats, empty or not. """
        self.counter = 0
        self.seat_tup = tuple(s for s in self.seats)
        return self

    def next(self):
        """ Move to the next seat in the iterator. """
        if self.counter > len(self.seat_tup) - 1:
            raise StopIteration
        p = self.seat_tup[self.counter]
        self.counter += 1
        return p

    def __contains__(self, player):
        """ Returns True if the player is occupying a seat at the table,
            False otherwise.
        """
        for s in self:
            if s.player == player:
                return True
        return False

    def add_player(self, index, player):
        """ Adds the player to the seat at the index.
            Returns True if successful, False otherwise.
        """
        # Check if the player is already sitting.
        if player.name in [s.player.name for s in iter(self) if s.occupied()]:
            return False

        if self.seats[index].vacant():
            self.seats[index].sitdown(player)
            return True
        else:
            return False

    def pop(self, index):
        """ Removes and returns a player from a given seat index. If the seat is
            empty, raises a ValueError exception.
        """
        s = self.seats[index]
        if s.vacant():
            raise ValueError('The seat is already empty!')
        else:
            p = s.standup()
            return p

    def get_index(self, player):
        """ Tries to find the player in the table and returns it's index.
            Returns -1 if it can't find the player.
        """
        for i, s in enumerate(self.seats):
            if s.player == player:
                return i
        return -1

    def get_free_seats(self):
        """ Returns a list of all seats that are vacant. """
        return [s for s in self if s.vacant()]

    def get_occupied_seats(self):
        """ Returns a list of all seats that are occupied. """
        return [s for s in self if s.occupied()]
