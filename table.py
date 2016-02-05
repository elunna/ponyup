from __future__ import print_function
import random

# Table class
# 4 types of tables, 2-handed, 6-handed, 9-handed, 10-handed
VALID_SIZES = [2, 6, 9, 10]


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
        return len(self.seats)

    def __str__(self):
        _str = '{:3}{:12}{:8}{:4}{:10}'.format('#', 'Player', 'Chips', '     ', 'Cards')
        _str += '\n-----------------------------------'
        _str += '\n'

        for i, s in enumerate(self.seats):
            if s is None:
                _str += '{}\n'.format(i)
            else:
                _str += '{:<3}{:12}${:<7}'.format(i, str(s), s.chips, )
                # Show button if it has been set
                if self.btn > 1 and i == self.btn:
                    _str += '[BTN]'
                else:
                    _str += ' '*4
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
        self.btn = random.randint(0, len(self.seats) - 1)

    def move_button(self):
        # Move the button to the next valid player/seat
        self.btn = self.next(self.btn)

    def get_players(self):
        # Sort players so the BTN is indexed at 0.
        if self.btn == 0:
            return self.seats
        else:
            return self.seats[self.btn:] + self.seats[0:self.btn]

    def next(self, from_seat):
        # Return the next available player from from_seat
        length = len(self.seats)

        for i in range(1, length + 1):
            currentseat = (from_seat + i) % length
            if self.seats[currentseat] is not None:
                return currentseat
        else:
            return -1


def test_table(testnum):
    table = Table(testnum)

    # Fill the table spots with the numbers they originally correspond with
    # This will aid in testing the get_playerlist function.
    for s in range(len(table)):
        table.add_player(s, s)

    print('Made a table of {} seats. actual seats: {}'.format(testnum, len(table)))
    print(table.seats)

    table.randomize_button()
    print('button position is {}'.format(table.btn))

    if table.btn > len(table):
        print('Button position is out of the table bounds!!!')

    print('Testing get_playerlist')
    pl = table.get_players()
    print(pl)
    print('Testing move_button(* denotes the BTN)')
    for i in range(10):
        table.move_button()
        for s in table.seats:
            print('{}'.format(s), end='')
            if table.btn == s:
                print('*', end='')
            print(' ', end='')
        print('')
    print('')


if __name__ == "__main__":
    # Tests

    for t in VALID_SIZES:
        test_table(t)
