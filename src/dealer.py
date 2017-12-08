class Dealer(object):
    def __init__(self, table):
        self.table = table

    def get_players(self, hascards=False, haschips=False):
        """ Returns a list of seats at the table. If the button is set, it is
            ordered from first after button, to Button Last. Can specify if seats
            have cards and/or chips.
        """
        if self.table.TOKENS['D'] == -1:
            btn = 0
        else:
            btn = self.table.TOKENS['D']

        length = len(self.table)
        first = (btn + 1) % length
        seats = list(range(first, length)) + list(range(first))

        seatlist = [self.table.seats[s] for s in seats if self.table.seats[s].occupied()]

        if hascards is True:
            seatlist = list(filter((lambda x: x.has_hand() == True), seatlist))

        if haschips is True:
            seatlist = list(filter((lambda x: x.has_chips() == True), seatlist))

        return seatlist

    def next_player(self, from_seat, step=1, hascards=False):
        """ Attempts to find the index of the next valid player from the from_seat.
            If step is -1 it will search backwards on the table. Step can only be
            1 or -1. We can also specify to search for the next player with cards
            by setting hascards to True. If no player is found after searching
            the length of the table, an exception is raised.
        """
        if from_seat < -1 or from_seat >= len(self.table):
            raise ValueError('from_seat is out of bounds!')
        if abs(step) != 1:
            raise ValueError('step needs to be 1 or -1.')

        length = len(self.table)
        for i in range(1, length + 1):
            _seat = (from_seat + (i * step)) % length
            s = self.table.seats[_seat]

            if s.vacant():
                continue
            elif hascards and not s.has_hand():
                continue
            return _seat

        raise Exception('Error finding player!')

    def get_broke_players(self):
        """ Returns a list of all the seats that have no chips in front of them. """
        return [s for s in self.table if s.occupied() and s.has_chips() is False]

    def get_playerdict(self):
        """ Returns a dictionary of seat indexes and players. """
        players = {}
        for i, s in enumerate(self.table.seats):
            if s.occupied():
                players[i] = s.player
        return players

    def stackdict(self):
        """ Returns a seat number/stacksize dictionary for each player at the table. """
        stacks = {}
        for s in self.table:
            stacks[s.NUM] = s.stack
        return stacks

    def stacklist(self):
        """ Returns a list of all the stack sizes. """
        return [s.stack for s in self.table]

    def player_listing(self):
        """ Returns the list of seats with players and stacks, for the hand history. """
        _str = ''
        for i, s in enumerate(self.table.seats):
            if s.player is None:
                _str += 'Seat #{}:\n'.format(i)
            else:
                _str += 'Seat #{}: {}(${})\n'.format(i, str(s.player), s.stack)
        return _str

    def position(self, _seat, postflop=False):
        """ Returns how many seats from the button the seat is. """
        # Raise an exception if the button is not set

        if postflop:
            seats = self.get_players(hascards=True)
        else:
            seats = self.get_players()

        return len(seats) - seats.index(_seat) - 1
