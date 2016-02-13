from __future__ import print_function
import random
import player
import names

# Table class
# 4 types of tables, 2-handed, 6-handed, 9-handed, 10-handed
VALID_SIZES = [2, 6, 9, 10]


class Table():
    def __init__(self, size):
        if size not in VALID_SIZES:
            print('Not a valid table size!')
            exit()  # Crash hard.

        self.TOKENS = {
            'ACTIVE': -1,
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
        # Return the number of players occupying seats
        num = len(self.seats)
        for s in self.seats:
            if s is None:
                num -= 0
        return num

    def horz_display(self):
        _str = ''
        # Seat # line
        for i, s in enumerate(self.seats):
            #  if s is not None:
            _str += 'Seat {:<5}'.format(i)
        _str += '\n'
        # Player line
        for i, s in enumerate(self.seats):
            if s is not None:
                _str += '{:<10}'.format(str(s))
        _str += '\n'
        # Chips line
        for i, s in enumerate(self.seats):
            if s is not None:
                _str += '${:<9}'.format(s.chips)
        _str += '\n'
        return _str

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

    def btn(self):
        return self.TOKENS['D']

    def get_sb(self):
        return self.seats[self.TOKENS['SB']]

    def get_bb(self):
        return self.seats[self.TOKENS['BB']]

    def active(self):
        return self.TOKENS['ACTIVE']

    def next_active(self):
        while True:
            n = self.next(self.active())

            if len(self.seats._hand) > 0:
                self.TOKENS['ACTIVE'] = n
                return self.seats[n]

    def add_player(self, s, p):
        """ Adds a player p to the table at seat s"""
        if self.seats[s] is None:
            self.seats[s] = p
        else:
            print('Seat {} is occupied.'.format(s))

    def remove_player(self, s):
        if self.seats[s] is not None:
            self.seats[s] = None
        else:
            print('Seat {} is already empty.'.format(s))

    def get_players(self):
        # Returns a list of all the active players at the table
        # If the button hasn't been set yet...
        if self.btn() < 0:
            self.randomize_button()

        # Sort players so the BTN is indexed at 0.
        players = self.seats[self.btn():] + self.seats[0:self.btn()]

        return [p for p in players if p is not None]

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

    def next(self, from_seat):
        # Return the next available player from from_seat
        length = len(self.seats)

        for i in range(1, length + 1):
            currentseat = (from_seat + i) % length
            if self.seats[currentseat] is not None:
                return currentseat
        else:
            return -1

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


def setup_table(num, hero=None):
    # The hero variable lets someone pass in a Human player name
    # If they don't want any human players, just let it be None.

    t = Table(num)
    nameset = names.generate_random_namelist(num)

    for i, s in enumerate(t.seats):
        if i == 0 and hero is not None:
            t.add_player(0, player.Player(hero, 'HUMAN'))
        elif nameset[-1] is not None:
            t.add_player(i, player.Player(nameset.pop(), 'CPU'))
        else:
            nameset.pop()
    return t


def test_table(testnum):
    #  t = Table(testnum)
    t = setup_table(testnum)
    t.randomize_button()
    print('-'*70)
    print('Made a table of {} seats. actual seats: {}'.format(testnum, len(t)))
    print('button position is {}'.format(t.btn()))
    print(t)
    if t.btn() > len(t):
        print('Button position is out of the table bounds!!!')

    # Test next
    btn_plus1 = t.next(t.btn())
    btn_plus2 = t.next(btn_plus1)
    print('next() from BTN is {}'.format(t.next(btn_plus1)))
    print('next() from BTN+1 is {}'.format(t.next(btn_plus2)))

    pl = t.get_players()
    print('get_playerlist: {} players'.format(len(pl)))
    print(pl)
    print('')

    print('Testing move_button(* = button)')
    for i in range(5):
        for i, s in enumerate(t.seats):
            print('{}'.format(s), end='')
            if t.btn() == i:
                print('*', end='')
            print(' ', end='')
        print('')
        t.move_button()
    print('')


if __name__ == "__main__":
    # Tests

    for t in VALID_SIZES:
        test_table(t)
