from __future__ import print_function
import table
import deck
import fivecarddraw
#  import tools
import game
import card
import blinds
#  import operator


class Game():
    def __init__(self, gametype, stakes, tablesize, hero=None):
        self.blinds = blinds.limit[stakes]
        self.rounds = 1
        self._table = table.setup_table(tablesize, hero)
        self._table.randomize_button()

    def __str__(self):
        _str = 'Round: {:<5} '.format(self.rounds)
        _str += 'Stakes: ${}/${}'.format(
            self.blinds[1], self.blinds[1] * 2).rjust(36)

        return _str

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

        if len(newround.players) > 1:
            newround.discard_phase()

            # Show table post draw
            #  print(self._table)

            # Post-draw betting round

            # Check for winners/showdown
            winners = newround.get_winner()

            # Award pot
            newround.award_pot(winners)

        else:
            newround.award_pot(newround.players)

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
        self.tbl = game._table

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
        for p in self.tbl:
            self.stacks[p.name] = p.chips

    def __str__(self):
        #  _str = 'Street {}\t'.format(self.street)
        _str = 'Pot: ${:}\n'.format(self.pot).rjust(50)
        return _str

    def check_for_stale_cards(self):
        #  Check that no players have lingering cards
        for p in self.tbl:
            if len(p._hand) > 0:
                raise ValueError('Player has cards when they should not!')

    def deal_hands(self):
        for i in range(5):
            for p in self.tbl:
                p.add(self.d.deal())

    def discard_phase(self):
        print('\nDiscard phase...')
        # Make sure the button goes last!
        holdingcards = self.tbl.card_holders()

        for p in holdingcards:

            ishuman = p.playertype == 'HUMAN'
            # Discard!
            if ishuman:
                discards = fivecarddraw.human_discard(p._hand)
            else:
                discards = fivecarddraw.auto_discard(p._hand)

            if discards:
                # Easier to put this here...
                if ishuman:
                    print('{:15} discards {}, draws: '.format(
                        str(p), discards), end='')
                else:
                    print('{:15} discards {}.'.format(
                        str(p), discards), end='')
            else:
                print('{:15} stands pat.'.format(p))

            # Redraw!
            for c in discards:
                self.muck.append(p.discard(c))

                draw = self.d.deal()
                if ishuman:
                    draw.hidden = False
                    print('{} '.format(draw), end='')

                p.add(draw)
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
            print('{:15} shows: {}'.format(
                str(p), p._hand))

        #  print('creating a list of value/player values')
        handlist = [(p._hand.value, p) for p in self.players]
        bestvalue = max(handlist)

        winners = [h[1] for h in handlist if h[0] == bestvalue[0]]

        print('-'*40)
        print('')
        if len(winners) == 1:
            #  print('The winner is: {}'.format(winners[0][1]))
            print('{} wins with a {} - {}'.format(
                #  winners[0][1], winners[0][1]._hand.handrank, winners[0][1]._hand.description))
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

    def ante_up(self):
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

        while len(self.players) > 1:
            p = self.players[self.bettor]
            #  o = None
            cost = self.betsize * self.level - (self.stacks[p.name] - p.chips)
            options = self.get_options(cost)

            if p.playertype == 'HUMAN':
                print(self)
                o = self.menu(options)
                self.process_option(o)

            elif p.playertype == 'CPU':
                o = p.makeplay(options)
                self.process_option(o)

            # This is complex and UGLY, we'll fix in the future
            if o[0] == 'FOLD' and self.bettor == self.closer:
                # Player folded just before the last player
                pass
            elif o[0] == 'FOLD' and self.bettor < len(self.players):
                # Don't further the position in the list,
                # the player was deleted from the player list.
                pass
            elif o[0] == 'FOLD' and self.bettor == len(self.players):
                # Last player was deleted from the player list.
                # next player should be 0
                self.bettor = 0
            elif self.bettor == self.closer:
                break
            else:
                self.bettor = self.nextbettor()
        else:
            print('Only one player left!')

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

            # This is necessary to offset the item removal in the list
            # It's ugly I know...
            if self.bettor < self.closer:
                self.closer -= 1

        elif option[2] > 0:
            # It's a raise, so we'll need to reset last better.
            self.closer = self.lastbettor()
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

    def nextbettor(self):
        return (self.bettor + 1) % len(self.players)

    def lastbettor(self):
        return (self.bettor - 1) % len(self.players)


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
    t = table.setup_table(len(hands))
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
