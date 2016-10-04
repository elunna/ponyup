from __future__ import print_function
import random
from ponyup import card
from ponyup import console
from ponyup import evaluator
from ponyup import seat

VALID_SIZES = list(range(2, 10))


class Table():
    def __init__(self, size):
        if size not in VALID_SIZES:
            raise ValueError('Not a valid table size!')

        self.TOKENS = {'D': -1, 'SB': -1, 'BB': -1, 'BI': -1}
        self.seats = [seat.Seat(i) for i in range(size)]

    def __str__(self):
        return console.display_table(self)

    def __len__(self):
        """
        Return the total # of seats.
        """
        return len(self.seats)

    def __iter__(self):
        """
        Creates an iterator for the table seats. Iterates over all seats, empty or not.
        """
        self.counter = 0
        self.seat_tup = tuple(s for s in self.seats)
        return self

    def __next__(self):
        """
        Move to the next seat in the iterator.
        """
        if self.counter > len(self.seat_tup) - 1:
            raise StopIteration
        p = self.seat_tup[self.counter]
        self.counter += 1
        return p

    def __contains__(self, player):
        """
        Returns True if the player is occupying a seat at the table, False otherwise.
        """
        for s in self:
            if s.player == player:
                return True
        else:
            return False

    def add_player(self, index, player):
        """
        Adds the player to the seat at the index.
        Returns True if successful, False otherwise.
        """
        # Check if the player is already sitting.
        if player.name in [s.player.name for s in self if s.occupied()]:
            return False

        if self.seats[index].vacant():
            self.seats[index].sitdown(player)
            return True
        else:
            return False

    def pop(self, index):
        """
        Removes and returns a player from a given seat index. If the seat is empty, raises a
        ValueError exception.
        """
        s = self.seats[index]
        if s.vacant():
            raise ValueError('The seat is already empty!')
        else:
            p = s.standup()
            return p

    def get_index(self, player):
        """
        Tries to find the player in the table and returns it's index. Returns -1 if it can't
        find the player.
        """
        for i, s in enumerate(self.seats):
            if s.player == player:
                return i
        else:
            return -1

    def get_players(self, hascards=False, haschips=False):
        """
        Returns a list of seats at the table. If the button is set, it is ordered from first
        after button, to Button Last. Can specify if seats have cards and/or chips.
        """
        if self.TOKENS['D'] == -1:
            btn = 0
        else:
            btn = self.TOKENS['D']

        length = len(self)
        first = (btn + 1) % length
        seats = list(range(first, length)) + list(range(first))

        seatlist = [self.seats[s] for s in seats if self.seats[s].occupied()]

        if hascards is True:
            seatlist = list(filter((lambda x: x.has_hand() == True), seatlist))

        if haschips is True:
            seatlist = list(filter((lambda x: x.has_chips() == True), seatlist))

        return seatlist

    def next_player(self, from_seat, step=1, hascards=False):
        """
        Attempts to find the index of the next valid player from the from_seat. If step is -1
        it will search backwards on the table. Step can only be 1 or -1. We can also specify to
        search for the next player with cards by setting hascards to True. If no player is found
        after searching the length of the table, an exception is raised.
        """
        if from_seat < -1 or from_seat >= len(self):
            raise ValueError('from_seat is out of bounds!')
        if abs(step) != 1:
            raise ValueError('step needs to be 1 or -1.')

        length = len(self)
        for i in range(1, length + 1):
            seat = (from_seat + (i * step)) % length
            s = self.seats[seat]

            if s.vacant():
                continue
            elif hascards and not s.has_hand():
                continue
            return seat

        else:
            raise Exception('Error finding player!')

    def get_broke_players(self):
        """
        Returns a list of all the seats that have no chips in front of them.
        """
        return [s for s in self if s.occupied() and s.has_chips() is False]

    def get_free_seats(self):
        return [s for s in self if s.vacant()]

    def get_playerdict(self):
        """
        Returns a dictionary of seat indexes and players.
        """
        players = {}
        for i, s in enumerate(self.seats):
            if s.occupied():
                players[i] = s.player
        return players

    def stackdict(self):
        """
        Returns a seat number/stacksize dictionary for each player at the table.
        """
        stacks = {}
        for s in self:
            stacks[s.NUM] = s.stack
        return stacks

    def stacklist(self):
        """
        Returns a list of all the stack sizes.
        """
        return [s.stack for s in self]

    def player_listing(self):
        """
        Returns the list of seats with players and stacks, for the hand history.
        """
        _str = ''
        for i, s in enumerate(self.seats):
            if s.player is None:
                _str += 'Seat #{}:\n'.format(i)
            else:
                _str += 'Seat #{}: {}(${})\n'.format(i, str(s.player), s.stack)
        return _str

    def move_button(self):
        """
        Moves the button to the next valid player/seat and sets the blinds.
        """
        self.TOKENS['D'] = self.next_player(self.TOKENS['D'])

    def set_blinds(self):
        if len(self.get_players()) == 2:
            self.TOKENS['SB'] = self.TOKENS['D']
            self.TOKENS['BB'] = self.next_player(self.TOKENS['D'])
        elif len(self.get_players()) > 2:
            self.TOKENS['SB'] = self.next_player(self.TOKENS['D'])
            self.TOKENS['BB'] = self.next_player(self.TOKENS['SB'])
        else:
            raise ValueError('Not enough players at the table!')

    def set_bringin(self):
        """
        Finds which player has the lowest showing card and sets that player to the bringin.
        Also sets the button the player to the right. If reverse is true, we find the highest
        card instead.
        """
        seat = None
        lowcard = card.Card('Z', 's')  # Start high

        for s in self:
            c = s.hand.get_upcards()[0]
            if c.rank < lowcard.rank:
                lowcard, seat = c, s
            elif c.rank == lowcard.rank:
                if card.SUITVALUES[c.suit] < card.SUITVALUES[lowcard.suit]:
                    lowcard, seat = c, s

        self.TOKENS['BI'] = seat.NUM
        self.TOKENS['D'] = self.next_player(self.TOKENS['BI'], -1)

        return '{} has the lowest showing card.'.format(seat.player)

    def randomize_button(self):
        """
        Places the button at a random player's seat. If there is no players at the table, it
        raises an Exception."
        """
        seats = list(self.get_playerdict().keys())
        if len(seats) == 0:
            raise Exception('Cannot place the button, no players at table!')
        choice = random.choice(seats)
        self.TOKENS['D'] = choice

    def position(self, seat, postflop=False):
        """
        Returns how many seats from the button the seat is.
        """
        # Raise an exception if the button is not set

        if postflop:
            seats = self.get_players(hascards=True)
        else:
            seats = self.get_players()

        return len(seats) - seats.index(seat) - 1
