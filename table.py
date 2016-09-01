from __future__ import print_function
import colors
import random

VALID_SIZES = list(range(1, 10))


class Table():
    def __init__(self, size):
        if size not in VALID_SIZES:
            raise ValueError('Not a valid table size!')

        self.TOKENS = {'D': -1, 'SB': -1, 'BB': -1}
        self.seats = []
        for i in range(size):
            self.seats.append(None)

    def __len__(self):
        """
        Return the total # of seats.
        """
        return len(self.seats)

    def __str__(self):
        """
        Return the string representation of the table.
        """
        _str = ''
        _str = colors.color('{:5}{:7}{:7}{:20}{:<17}{:16}\n'.format(
            'Seat', 'Blinds', 'Dealer', 'Player', 'Chips', 'Hand'), 'gray', STYLE='BOLD')

        for i, s in enumerate(self.seats):
            if s is None:
                # No player is occupying the seat
                _str += '{}\n'.format(i)
                continue
            else:
                _str += '{:<5}'.format(i)

            if self.TOKENS['SB'] == i:
                _str += colors.color('{:7}'.format('[SB]'), 'lightblue')
            elif self.TOKENS['BB'] == i:
                _str += colors.color('{:7}'.format('[BB]'), 'blue')
            else:
                _str += ' '*7

            if self.TOKENS['D'] == i:
                _str += colors.color('{:7}'.format('[D]'), 'purple')
            else:
                _str += ' '*7

            _str += '{:20}'.format(s.name)

            _str += colors.color('${:<16}'.format(s.chips), 'yellow')

            # Display hand if available
            if s._hand is not None:
                _str += '{:16}'.format(str(s._hand))
            _str += '\n'

        return _str

    def __iter__(self):
        """
        Creates an iterator for the table.
        """
        self.counter = 0
        self.players = [p for p in self.seats if p is not None]
        return self

    def __next__(self):
        """
        Move to the next item in the iterator.
        """
        if self.counter > len(self.players) - 1:
            raise StopIteration
        p = self.players[self.counter]
        self.counter += 1
        return p

    def add_player(self, s, p):
        """
        Adds a player p to the table at seat s. Returns True if successful, False otherwise.
        """
        # Check if the player is already sitting.
        for seat in self:
            if p.name == seat.name:
                return False

        if self.seats[s] is None:
            self.seats[s] = p
            return True
        else:
            return False

    def get_index(self, plyr):
        """
        Tries to find the player in the table and returns it's index. Returns -1 if it can't
        find the player.
        """
        for i, s in enumerate(self.seats):
            if s == plyr:
                return i
        else:
            return -1

    def __contains__(self, plyr):
        """
        Returns True if the player is occupying a seat at the table, False otherwise.
        """
        return plyr in self.seats

    def remove_player(self, index):
        """
        Removes and returns a player from a given seat index. If the seat is empty, raises a
        ValueError exception.
        """
        p = self.seats[index]
        if p is None:
            raise ValueError('The seat is already empty!')
        else:
            self.seats[index] = None
            return p

    def next_player(self, from_seat, step=1, hascards=False):
        if from_seat < -1 or from_seat >= len(self):
            raise ValueError('from_seat is out of bounds!')
        if abs(step) != 1:
            raise ValueError('step needs to be 1 or -1.')

        length = len(self)
        for i in range(1, length + 1):
            seat = (from_seat + (i * step)) % length
            p = self.seats[seat]

            if p is None:
                continue
            elif hascards and not p.has_cards():
                continue
            return seat

        else:
            raise Exception('Error finding player!')

    def move_button(self):
        # Move the button to the next valid player/seat
        # Also set the blinds appropriately!
        self.TOKENS['D'] = self.next_player(self.TOKENS['D'])

        if len(self.get_players()) == 2:
            self.TOKENS['SB'] = self.TOKENS['D']
            self.TOKENS['BB'] = self.next_player(self.TOKENS['D'])
        elif len(self.get_players()) > 2:
            self.TOKENS['SB'] = self.next_player(self.TOKENS['D'])
            self.TOKENS['BB'] = self.next_player(self.TOKENS['SB'])
        else:
            raise ValueError('Not enough players at the table!')

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

        # This will also set the blinds...
        self.move_button()

    def remove_broke(self):
        """
        Remove players with no chips from the table and return them in a list.
        """
        players = []
        for p in self:
            if p.chips == 0:
                i = self.get_index(p)
                players.append(self.remove_player(i))
        return players

    def get_players(self, CARDS=False, CHIPS=False):
        """
        Returns a list of players at the table, ordered from SB first to Button Last. Can
        specify if players have cards and/or chips.
        """
        # If the button has not been set, return an unordered list of players.
        if self.TOKENS['SB'] == -1 or self.TOKENS['BB'] == -1:
            return [s for s in self.seats if s is not None]

        sb = self.TOKENS['SB']
        seats = list(range(sb, len(self))) + list(range(sb))

        players = [self.seats[s] for s in seats if self.seats[s] is not None]

        if CARDS is True:
            players = list(filter((lambda x: x.has_cards() == True), players))

        if CHIPS is True:
            players = list(filter((lambda x: not x.is_allin() == True), players))

        return players

    def get_playerdict(self):
        """
        Returns a dictionary of seat indexes and player names.
        """
        players = {}
        for i, s in enumerate(self.seats):
            if s is not None:
                players[i] = s
        return players

    def stackdict(self):
        """
        Returns a name/stacksize dictionary for each player at the table.
        """
        stacks = {}
        for p in self:
            stacks[p.name] = p.chips
        return stacks
