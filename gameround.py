from __future__ import print_function
import deck
import game
import card
import blinds


class Round():
    def __init__(self, game):
        self._game = game
        self.street = 0
        self.pot = 0
        self.sidepots = {}
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
        self.bettor = None
        self.closer = None

        #  Remember starting stacks of all playerso
        self.betstack = {}
        self.startstack = {}
        for p in self.tbl:
            self.startstack[p.name] = p.chips

    def __str__(self):
        _str = 'Pot: ${:}'.format(self.pot).rjust(50)
        return _str

    def cheat_check(self):
        #  Check that no players have lingering cards
        for p in self.tbl:
            if len(p._hand) > 0:
                raise ValueError('Player has cards when they should not!')

    def deal_hands(self, qty):
        for i in range(qty):
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

    def cleanup(self):
        """ Remove players with no chips from the table. """
        for p in self.tbl:
            if p.chips == 0:
                i = self.tbl.player_index(p)
                self.tbl.remove_player(i)
                #  self.tbl.remove_player2(p)

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

        self.process_allins()

        if len(self.sidepots) == 0:
            # No sidepots!
            # Create a list of winners based on the best hand value found
            bestvalue = max(handlist)
            winners = [h[1] for h in handlist if h[0] == bestvalue[0]]

            print('-'*40)
            print('')

            self.award_pot(winners, self.pot)

        else:
            self.process_sidepots(handlist)

    def process_sidepots(self, handlist):
        # Organize the sidepots into an ascending sorted list.
        stacks_n_pots = sorted(
            [(p, self.sidepots[p]) for p in self.sidepots])
        #  stacks_n_pots = sorted(stacks_n_pots)

        # Test print the stacks_n_pots
        for x in stacks_n_pots:
            print(x)

        leftovers = self.pot

        # Go through and process the main pot first,
        # then the 1st sidepot, 2nd sidepot, etc.
        for i, pot in enumerate(sorted(stacks_n_pots)):
            potshare = 0
            # Calculate the pot
            if i == 0:
                potshare = pot[1]
                leftovers -= pot[1]
            else:
                lastpot = stacks_n_pots[i - 1][1]
                potshare = pot[1] - lastpot
                leftovers -= potshare

            self.segregate_eligible(handlist, potshare, pot[0])

        if leftovers > 0:
            # We'll pass potlist[1] + 1 so that all the elibigle players are
            # just above the largest allin.
            above_allin = max(stacks_n_pots)[0] + 1
            #  above_allin = max(stacks_n_pots[1]) + 1
            self.segregate_eligible(handlist, leftovers, above_allin)

    def segregate_eligible(self, handlist, potshare, minimumstack):
        eligible_players = [p for p in handlist
                            if self.startstack[p[1].name] >= minimumstack]

        print('Eligible players for the ${} pot'.format(potshare))
        print('\t', end='')

        bestvalue = 0
        for e in eligible_players:
            if e[0] > bestvalue:
                bestvalue = e[0]
            print('{} '.format(e[1]), end='')
        print('')

        winners = [h[1] for h in eligible_players if h[0] == bestvalue]

        self.award_pot(winners, potshare)

    def process_allins(self):
        for p in self.tbl.get_cardholders():
            # Look for allins and create sidepots
            if p.chips == 0:
                allin = self.startstack[p.name]

                self.make_sidepot(allin)

    def make_sidepot(self, stacksize):
        """
        How this function works:
        When the showdown is calculating the winners, it detects allin players
        and will send them here to create a sidepot.

        "Sidepot is a bit of a misnomer since it is actually how much the given stack size
        can win. The first side pot created will actually be the "main pot" that all players
        are eligible for. This system will make it easier to calculate the winnings at the end.
        """
        print('')
        if stacksize in self.sidepots:
            # There is already a sidepot for this stacksize
            return

        #  print('sidepot being created:')
        mainpot = 0

        # Go through the table of players
        for p in self.tbl:
            # For each player, get their total invested amount over the round
            invested = self.startstack[p.name] - p.chips

            # If stacksize is less than invested, they can only win the stacksize.
            if stacksize <= invested:
                # mainpot: add the allin stacksize
                mainpot += stacksize
            elif stacksize > invested:
                # if the allin stacksize is more than the invested,
                # they can win all the invested amount
                mainpot += invested

        self.sidepots[stacksize] = mainpot

    def award_pot(self, winners, amt):
        # If there are multiple winners, they must split the pot
        # If there is a remainder amount, we give it to the next left of the BTN.
        # (ie: Usually the SB)
        if len(winners) > 1:
            share = int(amt / len(winners))
            remainder = amt % len(winners)
        else:
            share = amt
            remainder = 0
        for w in winners:

            w.win(share)
            print('\t{} wins {} chips with a {}, {}'.format(
                w, share, w._hand.handrank, w._hand.description))

        if remainder > 0:
            r_winner = self.tbl.seats[self.tbl.next(self.tbl.btn)]
            print('\t{} wins {} remainder chips'.format(r_winner, remainder))

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
            self.betstack = self.startstack

        elif self.street > 0:
            # postflop the first bettor is right after the button
            self.level = 0
            self.betsize = self._game.blinds[1] * 2
            self.closer = self.tbl.prev(self.tbl.get_sb(), hascards=True)
            self.bettor = self.tbl.next(self.tbl.btn(), hascards=True)

            # Remember starting stack size.
            for p in self.tbl:
                self.betstack[p.name] = p.chips

    def betting(self):
        playing = True

        while playing:
            p = self.tbl.seats[self.bettor]
            invested = self.betstack[p.name] - p.chips
            cost = self.betsize * self.level - invested
            options = self.get_options(cost)

            if p.chips == 0:
                print('{} is all in.'.format(p))
            elif p.playertype == 'HUMAN':
                print(self)
                o = self.menu(options)
                self.process_option(o)

            elif p.playertype == 'CPU':
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


def test_stacks():
    myblinds = blinds.limit['50/100']
    g = game.Game('FIVE CARD DRAW', myblinds, 6, 'LUNNA')
    g._table.seats[0].chips = 100
    #  g._table.seats[1].chips = 150
    print(g)
    print(g._table)

    r = Round(g)
    r.deal_hands(5)
    print(r)

    bet = 200
    print('everybody bets {}!'.format(bet))
    for p in r.tbl:
        r.pot += p.bet(bet)

    print(r)

    r.process_allins()
    print('the lowest allin = {}'.format(min(r.sidepots)))
    print('the highest allin = {}'.format(max(r.sidepots)))
    print('')
    r.showdown()
    r.cleanup()
    print(r)
    #  print(g._table)
    print(r.tbl)

if __name__ == "__main__":
    # Perorm unit tests

    hc1 = [('A', 'h'), ('K', 's'), ('Q', 's'), ('J', 'd'), ('9', 'h')]
    hc2 = [('A', 's'), ('K', 'h'), ('Q', 'h'), ('J', 'h'), ('9', 'c')]
    test_winner(hc1, hc2)

    print('*'*80)
    hc1 = [('A', 'h'), ('A', 's'), ('K', 's'), ('Q', 'd'), ('J', 'h')]
    hc2 = [('A', 'c'), ('A', 'd'), ('K', 'h'), ('Q', 'h'), ('J', 'c')]
    test_winner(hc1, hc2)
