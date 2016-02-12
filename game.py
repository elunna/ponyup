from __future__ import print_function
import table
import deck
import fivecarddraw
import gametools
import game
import card
#  import operator

# blindstructures = [ante, sb, bb]

structures = {
    '2/4': (1, 2, .5),
    '3/6': (1, 3, 1),
    '4/8': (2, 4, 1),
    '6/12': (3, 6, 2),
    '8/16': (4, 8, 2),
    '10/20': (5, 10, 3),
    '15/30': (10, 15, 5),
    '20/40': (10, 20, 5),
    '30/60': (15, 30, 10),
    '50/100': (25, 50, 10),
}


class Game():
    def __init__(self, gametype, stakes, tablesize, hero=None):
        self.blinds = structures[stakes]
        self.rounds = 1
        self._table = table.setup_table(tablesize, hero)
        self._table.randomize_button()

    def __str__(self):
        return 'Round: {:<5} ${}/${}'.format(self.rounds, self.blinds[1], self.blinds[1] * 2)

    def playround(self):
        newround = Round(self)
        newround.check_for_stale_cards()

        # todo: Postblinds
        newround.post_blinds()

        # A simple 1-bet
        #  newround.ante_up()

        newround.deal_hands()

        # Show table pre draw
        print(newround)
        print(self._table)

        # Pre-draw betting round
        newround.setup_betting()
        newround.betting()

        newround.discard_phase()

        # Show table post draw
        #  print(self._table)

        # Post-draw betting round

        # Check for winners/showdown
        winners = newround.get_winner()

        # Award pot
        newround.award_pot(winners)

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
        self.betcap = 4
        self.betsize = 0
        self.level = 0

        self.muck = []
        self.d = deck.Deck()
        self.DECKSIZE = len(self.d)
        for i in range(3):
            self.d.shuffle()

        # Create a list of the players from the table, and place the button at index 0
        self.players = game._table.get_players()
        self.bettor = None
        self.closer = None

        #  Remember starting stacks of all playerso
        self.stacks = {}
        for p in self.players:
            self.stacks[p.name] = p.chips

    def __str__(self):
        _str = 'Round info: Street {}\n'.format(self.street)
        _str += 'Pot: ${}'.format(self.pot)
        return _str

    def check_for_stale_cards(self):
        #  Check that no players have lingering cards
        for p in self.players:
            if len(p._hand) > 0:
                raise ValueError('Player has cards when they should not!')

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
            print('{:15} holds {} with a: {}, {}'.format(
                str(p), p._hand, p._hand.handrank, p._hand.description))

        #  print('creating a list of value/player values')
        handlist = [(p._hand.value, p) for p in self.players]
        bestvalue = max(handlist)

        winners = [h for h in handlist if h[0] == bestvalue[0]]

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

    def award_pot(self, winners):
        if len(winners) == 1:
            p = winners[0][1]
            print('Player {} wins {} chips.'.format(p.name, self.pot))
            p.win(self.pot)

    def ante_up(self):
        # All players bet the ante amount and it's added to the pot
        for p in self.players:
            self.pot += p.bet(self._game.blinds[2])

    def post_blinds(self):
        # Preflop: Headsup
        sb, bb = -1, -1
        if self.street > 0:
            print('Blinds are not applicable past street 0!')
            exit()
        if len(self.players) == 2:
            sb, bb = 0, 1
        elif len(self.players) > 2:
            sb, bb = 1, 2
        elif len(self.players) < 2:
            raise ValueError('Not enough players to play!')
            exit()

        self.pot += self.players[sb].bet(self._game.blinds[0])
        self.pot += self.players[bb].bet(self._game.blinds[1])

        print('{} posts the small blind: ${}'.format(
            self.players[sb], self._game.blinds[0]))
        print('{} posts the big blind: ${}'.format(
            self.players[bb], self._game.blinds[1]))

    def setup_betting(self):
        # Set betsize, level, currentbettor and lastbettor
        # Preflop: Headsup
        if self.street == 0:
            if len(self.players) == 2:
                bb = 1
            else:
                #  sb, bb = 1, 2
                bb = 2
            self.level = 1
            self.betsize = self._game.blinds[1]
            self.closer = bb
            self.bettor = (bb + 1) % len(self.players)

        elif self.street > 0:
            self.level = 0
            self.betsize = self._game.blinds[1] * 2
            self.closer = 0
            self.bettor = 1

    def betting(self):

        while True:
            p = self.players[self.bettor]

            cost = self.betsize * self.level - (self.stacks[p.name] - p.chips)

            if p.playertype == 'HUMAN':
                options = self.get_options(cost)
                o = self.menu(options)
                self.process_option(o)

            elif p.playertype == 'CPU':
                if cost > 0:
                    self.pot += p.bet(cost)
                    print('\t{} bets ${}'.format(p.name, cost))
                elif cost == 0:
                    print('\t{} checks!'.format(p.name))

            if self.bettor == self.closer:
                break
            else:
                self.bettor = self.nextbettor()

    def process_option(self, option):
        #  print('The option passed was: {}'.format(option))
        #  print('Costs ${} and raises the betlevel by {}'.format(option[1], option[2]))

        p = self.players[self.bettor]

        if option[0] == 'FOLD':
            # Fold the players hand
            foldedcards = self.players[self.bettor].fold()
            self.muck.extend(foldedcards)
            # Remove the player from the active list
            self.players.remove(p)
        elif option[2] > 0:
            # It's a raise, so we'll need to reset last better.
            self.closer = self.lastbettor()
            self.pot += p.bet(option[1])
            self.level += option[2]

        print('\r{} {}\'s'.format(p, option[0]))

    def menu(self, options=None):
        # Sort by chip cost
        optlist = [(options[o][1], o, options[o][0][1:]) for o in options]

        print('(H)elp, (Q)uit')
        for o in sorted(optlist):
            print('({}){}--${} '.format(o[1], o[2], o[0]), end='')

        print('')
        while True:
            choice = input(':> ')

            if choice == 'q':
                exit()
            elif choice.lower() in options:
                return options[choice]
            else:
                print('Invalid choice, try again.')

    def get_options(self, cost):
        # Shows the options available to the current bettor
        completing = (self.betsize - cost) == self._game.blinds[0]

        OPTIONS = {}

        if self.street == 0 and completing:
            # Completing the small blind
            OPTIONS['f'] = ('FOLD', 0, 0)
            OPTIONS['c'] = ('COMPLETE', cost, 0)
            OPTIONS['r'] = ('RAISE', cost + self.betsize, 1)

        elif cost == 0 and self.level >= 1:
            # Typical BB, Straddle, or post situation.
            OPTIONS['c'] = ('CHECK', 0, 0)
            OPTIONS['r'] = ('RAISE', cost + self.betsize, 1)

        elif cost == 0 and self.level == 0:
            # Noone has opened betting yet on a postblind round
            OPTIONS['c'] = ('CHECK', 0, 0)
            OPTIONS['b'] = ('BET', self.betsize, 1)

        elif cost > 0 and self.level < self.betcap:
            # There has been a bet/raises, but still can re-raise
            OPTIONS['f'] = ('FOLD', 0, 0)
            OPTIONS['c'] = ('CALL', cost, 0)
            OPTIONS['r'] = ('RAISE', cost + self.betsize, 1)

        elif cost > 0 and self.level == self.betcap:
            # The raise cap has been met, can only call or fold.
            OPTIONS['f'] = ('FOLD', 0, 0)
            OPTIONS['c'] = ('CALL', cost, 0)

        return OPTIONS

    def nextbettor(self):
        return (self.bettor + 1) % len(self.players)

    def lastbettor(self):
        return (self.bettor - 1) % len(self.players)


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


def pick_name():
    print('Please enter your username.')
    while True:
        name = input(':> ')
        if len(name) > 15:
            print('Name is too long! Must be less than 15 characters.')
        else:
            break
    return name


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
