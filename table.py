from __future__ import print_function
import colors
import random

# Table class
# 4 types of tables, 2-handed, 6-handed, 9-handed, 10-handed
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
        # Return the total # of seats
        return len(self.seats)

    def __str__(self):
        _str = ''
        _str = colors.color('{:5}{:7}{:7}{:20}{:<17}{:16}\n'.format(
            'Seat', 'Blinds', 'Dealer', 'Player', 'Chips', 'Hand'), 'gray', STYLE='BOLD')

        for i, s in enumerate(self.seats):
            if s is None:
                # No player is occupying the seat
                _str += '{}\n'.format(i)
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
        self.counter = 0
        self.players = [p for p in self.seats if p is not None]
        return self

    def __next__(self):
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
        for i, s in enumerate(self.seats):
            if s == plyr:
                return i
        else:
            return -1

    def __contains__(self, plyr):
        return plyr in self.seats

    def remove_player(self, index):
        p = self.seats[index]
        if p is not None:
            self.seats[index] = None
        return p

    def get_players(self):
        # Returns a list of all the active players at the table
        return [p for p in self.seats if p is not None]

    def valid_bettors(self):
        count = 0
        for i in range(len(self)):
            if self.has_cards(i):
                count += 1
        return count

    def next(self, from_seat, step=1):
        length = len(self)
        if from_seat < -1 or from_seat >= len(self):
            raise ValueError('from_seat is out of bounds!')

        for i in range(1, length + 1):
            currentseat = (from_seat + (i * step)) % length
            p = self.seats[currentseat]

            if p is not None:
                return currentseat
        else:
            raise Exception('Error finding player!')

    # Find next valid player with cards to be the closer
    def next_player_w_cards(self, from_seat, step=1):
        seat = from_seat
        for i in range(len(self)):
            seat = self.next(seat, step)

            if self.has_cards(seat) and seat != from_seat:
                return seat
        else:
            raise Exception('Error finding player with cards!')

    def move_button(self):
        # Move the button to the next valid player/seat
        # Also set the blinds appropriately!
        self.TOKENS['D'] = self.next(self.TOKENS['D'])

        if len(self.get_players()) == 2:
            self.TOKENS['SB'] = self.TOKENS['D']
            self.TOKENS['BB'] = self.next(self.TOKENS['D'])
        elif len(self.get_players()) > 2:
            self.TOKENS['SB'] = self.next(self.TOKENS['D'])
            self.TOKENS['BB'] = self.next(self.TOKENS['SB'])
        else:
            raise ValueError('Not enough players at the table!')

    def get_playerdict(self):
        players = {}
        for i, s in enumerate(self.seats):
            if s is not None:
                players[i] = s
        return players

    def randomize_button(self):
        # Place the button at a random seat
        seats = list(self.get_playerdict().keys())
        choice = random.choice(seats)
        self.TOKENS['D'] = choice

        # This will also set the blinds...
        self.move_button()

    def get_cardholders(self):
        """
        Returns a list of players with cards, ordered by small blind first.
        """
        if self.TOKENS['SB'] < 0:
            raise Exception('Trying to get cardholders before blinds were set!')
        sb = self.TOKENS['SB']

        seats = list(range(len(self)))
        seats = seats[sb:] + seats[0:sb]
        return [self.seats[s] for s in seats if self.has_cards(s)]

    def has_cards(self, s):
        if self.seats[s] is not None:
            return len(self.seats[s]._hand) > 0
        else:
            return False

    def remove_broke(self):
        """ Remove players with no chips from the table. """
        players = []
        for p in self:
            if p.chips == 0:
                i = self.get_index(p)
                players.append(self.remove_player(i))
        return players

    def get_valuelist(self):
        """
        Find all the players with cards and return a list of hand values and player objects.
        """
        handlist = []
        for p in self.get_cardholders():
            handlist.append((p._hand.value, p))
        return handlist

    def valuelist2(self):
        """ Find all the players with cards and return a list of hand values. """
        return [p._hand.value for p in self._table.get_cardholders()]
