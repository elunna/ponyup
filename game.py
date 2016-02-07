from __future__ import print_function
import table
import deck
import fivecarddraw
import gametools
import game
import card

# blindstructures = [ante, sb, bb]

structures = {
    '2/4': (1, 2),
    '3/6': (1, 3),
    '4/8': (2, 4),
    '6/12': (3, 6),
    '8/16': (4, 8),
    '10/20': (5, 10),
    '15/30': (10, 15),
    '20/40': (10, 20),
    '30/60': (10, 30),
    '50/100': (20, 50),
}


class Game():
    def __init__(self, struct, table):
        self.blinds = structures[struct]
        self._table = table
        self.betcap = 4
        self.rounds = 1

    def __str__(self):
        #  display = 'Game details\n'
        display = ''
        #  display += 'Blinds: {}/{}\n'.format(self.blinds[1], self.blinds[2])
        display += 'Stakes: ${}/${}\n'.format(self.blinds[1], self.blinds[1] * 2)
        #  display += 'Bet cap limit: {}\n'.format(self.betcap)
        #  display += 'Table size: {}\n'.format(len(self.table))
        display += 'Round: {}\n'.format(self.rounds)
        return display

    def get_stacks(self):
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
            startingstacks[i] = self._table.seats[i].chips
        return startingstacks

    def playround(self):

        newround = Round(self)

        newround.check_for_stale_cards()

        # todo: Postblinds

        newround.deal_hands()

        # Pre-draw betting round

        # Show table post draw
        print(self._table)

        newround.discard_phase()

        # Show table post draw
        #  print(self._table)

        # Post-draw betting round

        # Check for winners/showdown
        newround.get_winner()

        # Award pot

        # ================== CLEANUP
        newround.verify_muck()

        # Move the table button
        self._table.move_button()

        # Advance round counter
        self.rounds += 1


class Round():
    def __init__(self, game):
        self._game = game
        self.street = 0
        self.pot = 0
        self.muck = []

        self.d = deck.Deck()
        self.DECKSIZE = len(self.d)
        for i in range(3):
            self.d.shuffle()

        # Create a list of the players from the table, and place the button at index 0
        self.players = game._table.get_players()

        #  Remember starting stacks of all playerso
        self.startingstacks = []

    def post_blinds(self):
        pass

    def check_for_stale_cards(self):
        pass
        # Check that no players have lingering cards
        #  print('displaying hand lengths')
        #  for p in self.players:
            #  print(len(p._hand))
            #  if p is not None:
                #  if len(p._hand) > 0:
                    #  raise ValueError('Player has cards when they should not!')

    def deal_hands(self):
        for i in range(5):
            for p in self.players:
                p.add(self.d.deal())

    def discard_phase(self):
        print('\nDiscard phase...')
        # Make sure the button goes last!
        for i in range(1, len(self.players) + 1):
            plyr = i % len(self.players)

            ishuman = self.players[plyr].playertype == 'HUMAN'
            # Discard!
            if ishuman:
                discards = fivecarddraw.human_discard(self.players[plyr]._hand)
            else:
                discards = fivecarddraw.auto_discard(self.players[plyr]._hand)

            if discards:
                # Easier to put this here...
                if ishuman:
                    print('{:15} discards {}, draws: '.format(
                        str(self.players[plyr]), discards), end='')
                else:
                    print('{:15} discards {}.'.format(
                        str(self.players[plyr]), discards), end='')
            else:
                print('{:15} stands pat.'.format(str(self.players[plyr])))

            # Redraw!
            for c in discards:
                self.muck.append(self.players[plyr].discard(c))

                draw = self.d.deal()
                if ishuman:
                    draw.hidden = False
                    print('{} '.format(draw), end='')

                self.players[plyr].add(draw)
            print('')
        print('')

    def verify_muck(self):
        # Clear hands
        for p in self.players:
            self.muck.extend(p.fold())
        #  print('muck size = {}'.format(len(self.muck)))
        #  print('adding the remainder of the deck')
        # Add the remainder of the deck
        self.muck.extend(self.d.cards)
        #  print('muck size = {}'.format(len(self.muck)))
        if len(self.muck) != self.DECKSIZE:
            raise ValueError('Deck became corrupted! Muck doesn\'t equal starting deck!')
            exit()

    def get_winner(self):
        """
        Takes in a list of Players and determines who has the best hand
        * Should we return just the Player?
        """

        # Un-hide all cards involved in a showdown.
        for p in self.players:
            p.showhand()

        for i, p in enumerate(self.players):
            print('{:15} holds {} with a: {}'.format(
                str(p), p._hand, p._hand.handrank))

        #  print('creating a list of value/player values')
        handlist = [(p._hand.value, p) for p in self.players]
        #  print(handlist)

        #  bestvalue = max(handlist, key=lambda x: handlist[0])
        bestvalue = max(handlist)
        #  print('best value is {}'.format(bestvalue))

        winners = []
        for h in handlist:
            if h[0] == bestvalue[0]:
                winners.append(h)

        print('-'*40)
        print('')
        if len(winners) == 1:
            print('The winner is: {}'.format(winners[0][1]))
        elif len(winners) > 1:
            print('We have a TIE!')
            print('The winners are:', end='')
            for w in winners:

                print('{}, '.format(w[1]), end='')

        return winners


def pick_limit():
    print('Please enter what limit you want to play:(default 2/4)')

    struct_list = sorted(structures.keys())
    for l in struct_list:
        print('{}, '.format(l), end='')

    choice = input(':> ')
    if choice in structures:
        print('You selected {}'.format(choice))
        return structures[choice]
    else:
        print('Selection not available, going with default blinds: 2/4')
        return structures['2/4']


def pick_table():
    print('What size table do you want to play? (default is 2 seats)')

    for l in table.VALID_SIZES:
        print('{}, '.format(l), end='')

    choice = input(':> ')
    if int(choice) in table.VALID_SIZES:
        print('You selected {}'.format(choice))
        return choice
    else:
        print('Selection not available, going with default: 2 seats')
        return 2


def calculate_odds(bet, pot):
    print('first draft')
    print('Bet = {}, pot = {}'.format(bet, pot))
    #  diff = pot - bet
    print('bet is {}% of the pot'.format(bet/pot * 100))

    odds = pot / bet
    print('The odds are {}-to-1'.format(odds))
    return odds


def test_winner(*hands):
    print('Test player ties')
    t = gametools.setup_test_table(len(hands))
    g = game.Game('2/4', t)
    t.randomize_button()

    newround = Round(g)
    #  hc1 = [('A', 'h'), ('K', 's'), ('Q', 's'), ('J', 'd'), ('9', 'h')]
    #  hc2 = [('A', 's'), ('K', 'h'), ('Q', 'h'), ('J', 'h'), ('9', 'c')]
    for i in range(len(hands)):

        for c in hands[i]:
            newround.players[i].add(card.Card(c[0], c[1]))

    # Print test info
    print(g)
    print(t)
    for p in newround.players:
        print('Player 0: {}'.format(p._hand.value))

    winners = newround.get_winner()
    print('')
    print('Winners list:')
    print(winners)

if __name__ == "__main__":
    # Perorm unit tests

    hc1 = [('A', 'h'), ('K', 's'), ('Q', 's'), ('J', 'd'), ('9', 'h')]
    hc2 = [('A', 's'), ('K', 'h'), ('Q', 'h'), ('J', 'h'), ('9', 'c')]
    test_winner(hc1, hc2)
    print('*'*80)
    hc1 = [('A', 'h'), ('A', 's'), ('K', 's'), ('Q', 'd'), ('J', 'h')]
    hc2 = [('A', 'c'), ('A', 'd'), ('K', 'h'), ('Q', 'h'), ('J', 'c')]
    test_winner(hc1, hc2)
