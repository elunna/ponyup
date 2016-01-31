import deck
import table
import player
import random

# blindstructures = [ante, sb, bb]
structures = {}
structures['2/4'] = [0, 2, 4]
structures['3/6'] = [0, 3, 6]
structures['4/8'] = [0, 4, 8]


class Game():
    def __init__(self, struct, mytable):
        self.blinds = structures[struct]
        self.table = mytable
        self.betcap = 4
        self.rounds = 0

    def __str__(self):
        display = 'Game details\n'
        display += 'Blinds: {}/{}\n'.format(self.blinds[1], self.blinds[2])
        display += 'Bet cap limit: {}\n'.format(self.betcap)
        display += 'Table size: {}\n'.format(len(self.table))
        display += 'Current Round: {}\n'.format(self.rounds)
        return display

    def get_startingstacks(self):
        # Create a list(or tuple) beginning with the button that contains:
        # seat, username, chips
        """
        startingstacks = []
        num_players = len(table)
        c = table.btn
        for i in range(num_players):
            #  currentindex = (num_players + i) % num_players
            startingstacks.append(tuple(
                currentseatable.seats[currentindex])

        #  return self.table.seats
        """
        startingstacks = {}
        for i in len(table):
            startingstacks[i] = self.table.seats[i].chips
        return startingstacks


def dealhand(quantity):
    # Deal a regular 5 card hand from a new deck
    d = deck.Deck()
    d.shuffle()
    #  dealtcards = [d.deal() for i in range(quantity)]
    #  newhand = hand.Hand(dealtcards)
    #  return newhand
    return [d.deal() for i in range(quantity)]


def deal_players(players, handsize):
    """
    Returns a list of hands according to how many players are specified and how large
    the hands should be
    """

    # Check that the requirements of the players and handsizes don't over deplete the deck
    if players * handsize > 52:
        print('The required players and hand sizes would deplete the deck below negative!')
        return ValueError()

    playerlist = []
    d = deck.Deck()
    d.shuffle()

    for i in range(players):
        playerlist.append(None)
        playerlist[i] = [d.deal() for i in range(handsize)]

    # Verify hand sizes
    for p in playerlist:
        if not len(p) == handsize:
            print('Corrupt player decks, uneven starting numbers.')
            exit()

    return playerlist


def setup_test_table(num):

    names = ['Seidel', 'Doyle', 'Mercier', 'Negreanu', 'Grospellier', 'Hellmuth', 'Mortensen',
             'Antonius', 'Harman', 'Ungar', 'Dwan', 'Greenstein', 'Chan', 'Moss', 'Ivey',
             'Brunson', 'Reese', 'Esfandiari', 'Juanda', 'Duhamel', 'Gold', 'Cada', 'Mizrachi',
             'Schulman', 'Selbst', 'Duke', 'Rousso', 'Liebert', 'Galfond', 'Elezra',
             'Benyamine', 'Booth', 'D Agostino', 'Eastgate', 'Farha', 'Ferguson', 'Forrest',
             'Hansen', 'Hachem', 'Kaplan', 'Laak', 'Lederer', 'Lindren', 'Matusow', 'Minieri']

    t = table.Table(num)

    nameset = []
    for i in range(num):
        #  t.add_player(i, player.Player(names.pop()))

        # Make sure all the names are unique
        while True:
            nextname = random.choice(names)
            if nextname not in nameset:
                nameset.append(nextname)
                break

    for i, n in enumerate(nameset):
        t.add_player(i, player.Player(n))

    return t


def get_winner(players):
    """
    Takes in a list of Players and determines who has the best hand
    * Should we return just the Player?
    """

    # besthand tuple is (player index, hand value)
    besthand = {'player': -1, 'value': -1}

    for i, p in enumerate(players):
        print('Player#{}: {}'.format(i, p.display()))

        if players[i].value > besthand['value']:
            besthand['value'] = players[i].value
            besthand['player'] = i
    print('')
    print('')
    print('The player with the best hand is: {}'.format(besthand['player']))
    print('The best hand is:                 {}'.format(players[besthand['player']].display()))
    print('Type: {}'.format(players[besthand['player']].handrank))


def print_playerlist(players):
    for i, p in enumerate(players):
        print('{}: {}({})'.format(i, p, p.chips))


if __name__ == "__main__":
    # Tests
    print('Testing table setup')
    """
    t = setup_test_table(2)
    print(t)

    t = setup_test_table(6)
    print(t)

    t = setup_test_table(9)
    print(t)
    """

    t = setup_test_table(10)
    print(t)

    print('#'*80)
    print('Testing table get_players')
    print('Setting a random button')
    t.randomize_button()
    #  p = t.get_players()
    #  print_playerlist(p)
    print(t)

    t.remove_player(0)
    t.remove_player(1)
    print(t)

    print('Next player from 0: {}'.format(t.next(0)))
    print('Next player from 2: {}'.format(t.next(2)))

    t.remove_player(3)
    t.remove_player(5)
    print(t)

    print('Next player from 2: {}'.format(t.next(2)))
    print('Next player from 9: {}'.format(t.next(9)))

    print('#'*80)
    print('testing the button movement')
    for i in range(10):
        t.move_button()
        print(t)
