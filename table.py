from __future__ import print_function
import random
import player

# Table class
# 4 types of tables, 2-handed, 6-handed, 9-handed, 10-handed
VALID_SIZES = [2, 6, 9, 10]

names = ['Seidel', 'Doyle', 'Mercier', 'Negreanu', 'Grospellier', 'Hellmuth', 'Mortensen',
         'Antonius', 'Harman', 'Ungar', 'Dwan', 'Greenstein', 'Chan', 'Moss', 'Ivey', 'Brunson',
         'Reese', 'Esfandiari', 'Juanda', 'Duhamel', 'Gold', 'Cada', 'Mizrachi', 'Schulman',
         'Selbst', 'Duke', 'Rousso', 'Liebert', 'Galfond', 'Elezra', 'Benyamine', 'Booth',
         'DAgostino', 'Eastgate', 'Farha', 'Ferguson', 'Forrest', 'Hansen', 'Hachem', 'Kaplan',
         'Laak', 'Lederer', 'Lindren', 'Matusow', 'Minieri']


class Table():
    def __init__(self, size):
        if size not in VALID_SIZES:
            print('Not a valid table size!')
            exit()  # Crash hard.

        self.seats = []
        for i in range(size):
            self.seats.append(None)

        self.btn = -1

    def __len__(self):
        # Return the number of players occupying seats
        num = len(self.seats)
        for s in self.seats:
            if s is None:
                num -= 0
        return num

    def __str__(self):
        _str = '{:3}{:4}{:12}{:6}{:8}{:4}{:10}'.format(
            '#', 'BTN', 'Player', 'Type', 'Chips', '     ', 'Cards')
        _str += '\n-----------------------------------\n'

        for i, s in enumerate(self.seats):
            if s is None:
                # No player is occupying the seat
                _str += '{}\n'.format(i)
            else:
                _str += '{:<3}'.format(i)

                # Display button if it has been set
                if self.btn >= 0 and i == self.btn:
                    _str += '[D] '
                else:
                    _str += ' '*4

                _str += '{:12}{:6}${:<7}'.format(str(s), s.playertype, s.chips, )

                # Display hand if available
                if s._hand is not None:
                    _str += str(s._hand)
                _str += '\n'

        return _str

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

    def randomize_button(self):
        # Place the button at a random seat
        place = random.randint(0, len(self.seats) - 1)
        for i in range(place):
            self.btn = self.next(self.btn)

    def move_button(self):
        # Move the button to the next valid player/seat
        self.btn = self.next(self.btn)

    def get_players(self):
        # Sort players so the BTN is indexed at 0.
        if self.btn < 0:
            self.randomize_button()

        players = self.seats[self.btn:] + self.seats[0:self.btn]
        return [p for p in players if p is not None]

    def next(self, from_seat):
        # Return the next available player from from_seat
        length = len(self.seats)

        for i in range(1, length + 1):
            currentseat = (from_seat + i) % length
            if self.seats[currentseat] is not None:
                return currentseat
        else:
            return -1


def generate_random_namelist(num):
    nameset = []

    for i in range(num):
        # We'll use a 66% chance that a seat will be filled
        # So we can test the gaps/skipping/etc.
        chance = random.randint(0, 10)
        if chance < 7:
            # Make sure all the names are unique
            while True:
                nextname = random.choice(names)
                if nextname not in nameset:
                    nameset.append(nextname)
                    break
        else:
            nameset.append(None)
    return nameset


def setup_test_table(num, hero=None):
    # The hero variable lets someone pass in a Human player name
    # If they don't want any human players, just let it be None.

    #  import pdb
    #  pdb.set_trace()

    t = Table(num)
    nameset = generate_random_namelist(num)

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
    t = setup_test_table(testnum)

    t.randomize_button()
    print('button position is {}'.format(t.btn))

    print('Made a table of {} seats. actual seats: {}'.format(testnum, len(t)))
    print(t.seats)

    if t.btn > len(t):
        print('Button position is out of the table bounds!!!')

    print('Testing get_playerlist')
    pl = t.get_players()
    print('There are {} players'.format(len(pl)))
    print(pl)
    print('')
    print('Testing move_button(* = button)')
    for i in range(5):
        t.move_button()
        for i, s in enumerate(t.seats):
            print('{}'.format(s), end='')
            if t.btn == i:
                print('*', end='')
            print(' ', end='')
        print('')
    print('')

    print(t)

if __name__ == "__main__":
    # Tests

    for t in VALID_SIZES:
        test_table(t)
