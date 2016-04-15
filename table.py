from __future__ import print_function
import random
import player
import names
import strategy

# Table class
# 4 types of tables, 2-handed, 6-handed, 9-handed, 10-handed
VALID_SIZES = [2, 6, 9, 10]


class Table():
    def __init__(self, size):
        if size not in VALID_SIZES:
            raise ValueError('Not a valid table size!')

        self.TOKENS = {
            'D': -1,
            'SB': -1,
            'BB': -1,
            'STRADDLE': -1,
            'KILL': -1,
            'LEGUP': -1,
            'POST': None,
            'MISSED BLINDS': None,
            'SITTING OUT': None
        }

        self.seats = []
        for i in range(size):
            self.seats.append(None)

    def __len__(self):
        # Return the total # of seats
        return len(self.seats)

    def __str__(self):
        _str = '{:3}{:7}{:15}{:10}{:10}\n'.format(
            '#', 'Tokens', 'Player', 'Chips', 'Hand')
        #  _str += '\n--------------------------------------------------\n'
        _str += '-'*50
        _str += '\n'

        for i, s in enumerate(self.seats):
            if s is None:
                # No player is occupying the seat
                _str += '{}\n'.format(i)
            else:
                _str += '{:<3}'.format(i)

                tokens = ''
                for t in self.TOKENS:
                    if self.TOKENS[t] == i:
                        tokens += '[{}]'.format(t)
                _str += '{:7}{:15}${:<9}'.format(tokens, str(s), s.chips, )

                # Display hand if available
                if s._hand is not None:
                    _str += str(s._hand)
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

    def btn(self):
        return self.TOKENS['D']

    def get_sb(self):
        return self.TOKENS['SB']

    def get_bb(self):
        return self.TOKENS['BB']

    def add_player(self, s, p):
        """ Adds a player p to the table at seat s"""
        for seat in self:
            if p.name == seat.name:
                raise ValueError('Player {} is already at the table!'.format(p))

        if self.seats[s] is None:
            self.seats[s] = p
        else:
            raise ValueError('Seat {} is occupied.'.format(s))

    def get_index(self, plyr):
        #  return self.seats.index(plyr)
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

    def get_players(self):
        # Returns a list of all the active players at the table
        # If the button hasn't been set yet...
        if self.btn() < 0:
            self.randomize_button()

        # Sort players so the BTN is indexed at 0.
        players = self.seats[self.btn():] + self.seats[0:self.btn()]

        return [p for p in players if p is not None]

    def valid_bettors(self):
        count = 0
        for i in range(len(self)):
            if self.has_cards(i):
                count += 1
        return count

    def next(self, from_seat, step=1):
        if from_seat < -1 or from_seat >= len(self):
            raise ValueError('from_seat is out of bounds!')

        length = len(self)

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
        self.TOKENS['D'] = self.next(self.btn())

        if len(self) == 2:
            self.TOKENS['SB'] = self.btn()
            self.TOKENS['BB'] = self.next(self.btn())
        elif len(self) > 2:
            self.TOKENS['SB'] = self.next(self.btn())
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
        sb = self.get_sb()
        seats = list(range(len(self)))
        seats = seats[sb:] + seats[0:sb]

        return [self.seats[s] for s in seats if self.has_cards(s)]

    def has_cards(self, s):
        return len(self.seats[s]._hand) > 0


def setup_table(num, hero=None, gametype="DRAW5"):
    # The hero variable lets someone pass in a Human player name
    # If they don't want any human players, just let it be None.

    t = Table(num)
    nameset = names.generate_random_namelist(num)

    for i, s in enumerate(t.seats):
        if i == 0 and hero is not None:
            t.add_player(0, player.Player(hero, 'HUMAN'))
        elif nameset[-1] is not None:
            t.add_player(i, player.Player(nameset.pop(), 'CPU'))
            if gametype == "DRAW5":
                t.seats[i].strategy = strategy.get_reg_draw5()
        else:
            nameset.pop()
    return t
