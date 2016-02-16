from __future__ import print_function
import table
import deck
import draw5
import game
import card
import blinds


class Game():
    def __init__(self, gametype, stakes, tablesize=6, hero=None):
        self.blinds = blinds.limit[stakes]
        self.rounds = 1
        self._table = table.setup_table(tablesize, hero)
        self._table.randomize_button()

    def __str__(self):
        _str = 'Round: {:<5} '.format(self.rounds)
        _str += 'Stakes: ${}/${}'.format(
            self.blinds[1], self.blinds[1] * 2).rjust(36)

        return _str

    def play(self):
        newround = Round(self)
        newround.cheat_check()

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
        victor = newround.betting()

        if victor is None:
            #  newround.discard_phase()
            newround.muck.extend(draw5.discard_phase(self._table, newround.d))

            # Show table post draw
            print(self._table)

            # Post-draw betting round
            newround.setup_betting()
            victor = newround.betting()

            if victor is None:
                # Check for winners/showdown
                winners = newround.showdown()

                # Award pot
                newround.award_pot(winners)
            else:
                newround.award_pot(victor)
        else:
            newround.award_pot(victor)

        # ================== CLEANUP
        newround.check_muck()

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
        self.tbl = game._table

        self.muck = []
        self.d = deck.Deck()
        self.DECKSIZE = len(self.d)
        for i in range(3):
            self.d.shuffle()

        # Create a list of the players from the table, and place the button at index 0
        #  self.players = game._table.get_players()
        self.bettor = None
        self.closer = None

        #  Remember starting stacks of all playerso
        self.stacks = {}
        for p in self.tbl:
            self.stacks[p.name] = p.chips

    def __str__(self):
        #  _str = 'Street {}\t'.format(self.street)
        _str = 'Pot: ${:}\n'.format(self.pot).rjust(50)
        return _str

    def cheat_check(self):
        #  Check that no players have lingering cards
        for p in self.tbl:
            if len(p._hand) > 0:
                raise ValueError('Player has cards when they should not!')

    def deal_hands(self):
        for i in range(5):
            for p in self.tbl:
                p.add(self.d.deal())

    def check_muck(self):
        # Clear hands
        for p in self.tbl:
            self.muck.extend(p.fold())
        # Add the remainder of the deck
        self.muck.extend(self.d.cards)
        if len(self.muck) != self.DECKSIZE:
            raise ValueError('Deck is corrupted! Muck doesn\'t equal starting deck!')
            exit()

    def showdown(self):
        """
        Takes in a list of Players and determines who has the best hand
        * Should we return just the Player?
        """

        handlist = []
        # Un-hide all cards involved in a showdown.
        for p in self.tbl.get_cardholders():
            p.showhand()
            print('{:15} shows: {}'.format(str(p), p._hand))

            # Creating a list of value/player values')
            handlist.append((p._hand.value, p))

        # Create a list of winners based on the best hand value found
        bestvalue = max(handlist)
        winners = [h[1] for h in handlist if h[0] == bestvalue[0]]

        print('-'*40)
        print('')
        if len(winners) == 1:
            print('{} wins with a {} - {}'.format(
                winners[0], winners[0]._hand.handrank, winners[0]._hand.description))
        elif len(winners) > 1:
            print('We have a TIE!')
            print('The winners are:', end='')
            for w in winners:
                print('{}, '.format(w), end='')

        return winners

    def award_pot(self, winners):
        if len(winners) == 1:
            p = winners[0]
            print('{} wins {} chips.'.format(p.name, self.pot))
            p.win(self.pot)

    def post_antes(self):
        # All players bet the ante amount and it's added to the pot
        for p in self.tbl:
            self.pot += p.bet(self._game.blinds[2])

    def post_blinds(self):
        # Preflop: Headsup
        if len(self.tbl) < 2:
            raise ValueError('Not enough players to play!')
            exit()
        sb = self.tbl.seats[self.tbl.get_sb()]
        bb = self.tbl.seats[self.tbl.get_bb()]

        self.pot += sb.bet(self._game.blinds[0])
        self.pot += bb.bet(self._game.blinds[1])

        print('{} posts ${}'.format(sb, self._game.blinds[0]))
        print('{} posts ${}'.format(bb, self._game.blinds[1]))

    def setup_betting(self):
        # Set betsize, level, currentbettor and lastbettor
        # Preflop: Headsup
        if self.street == 0:
            # Preflop the first bettor is right after the BB
            self.level = 1
            self.betsize = self._game.blinds[1]
            self.closer = self.tbl.get_bb()
            self.bettor = self.tbl.next(self.closer)

        elif self.street > 0:
            # postflop the first bettor is right after the button
            self.level = 0
            self.betsize = self._game.blinds[1] * 2
            self.closer = self.tbl.prev(self.tbl.get_sb(), hascards=True)
            self.bettor = self.tbl.next(self.tbl.btn(), hascards=True)

            # Remember starting stack size.
            for p in self.tbl:
                self.stacks[p.name] = p.chips

    def betting(self):
        playing = True

        while playing:
            p = self.tbl.seats[self.bettor]
            invested = self.stacks[p.name] - p.chips
            cost = self.betsize * self.level - invested
            options = self.get_options(cost)

            if p.chips == 0:
                print('{} is all in.'.format(p))
            elif p.playertype == 'HUMAN':
                print(self)
                o = self.menu(options)
                self.process_option(o)

            elif p.playertype == 'CPU':
                #  print('{}\'s cost: ${}'.format(p, cost))
                o = p.makeplay(options, self.street)
                self.process_option(o)

            if self.tbl.valid_bettors() == 1:
                print('Only one player left!')
                winner = self.tbl.seats[self.tbl.next(self.bettor, True)]
                return [winner]

            elif self.bettor == self.closer:
                # Reached the last bettor, betting is closed.
                playing = False
            else:
                # Set next bettor
                self.bettor = self.tbl.next(self.bettor, hascards=True)

        else:
            self.street += 1
            return None

    def process_option(self, option):
        p = self.tbl.seats[self.bettor]

        if option[0] == 'FOLD':
            # Fold the players hand
            foldedcards = p.fold()
            self.muck.extend(foldedcards)

        elif option[2] > 0:
            # It's a raise, so we'll need to reset last better.
            self.closer = self.tbl.prev(self.bettor, hascards=True)
            self.pot += p.bet(option[1])
            self.level += option[2]
        else:
            self.pot += p.bet(option[1])

        print('\r{} {}s'.format(p, option[0].lower()))

    def menu(self, options=None):
        # Sort by chip cost
        optlist = [(options[o][1], o, options[o][0][1:]) for o in options]

        #  print('(H)elp, (Q)uit')
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


def calc_odds(bet, pot):
    print('first draft')
    print('Bet = {}, pot = {}'.format(bet, pot))
    #  diff = pot - bet
    print('bet is {}% of the pot'.format(bet/pot * 100))

    odds = pot / bet
    print('The odds are {}-to-1'.format(odds))
    return odds


def test_winner(*hands):
    print('Test player ties')
    g = game.Game('FIVE CARD DRAW', '2/4', 2)

    newround = Round(g)

    h1 = [card.Card(c[0], c[1]) for c in hands[0]]
    h2 = [card.Card(c[0], c[1]) for c in hands[1]]

    newround.tbl.seats[0]._hand.cards = h1
    newround.tbl.seats[0]._hand.update()
    newround.tbl.seats[1]._hand.cards = h2
    newround.tbl.seats[1]._hand.update()

    # Print test info
    print(g)
    print(g._table)

    for p in newround.tbl:
        print('Player 0: {}'.format(p._hand.value))

    winners = newround.showdown()
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
