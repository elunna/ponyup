from __future__ import print_function
import betting
import colors
import deck
import setup_table
import strategy

STARTINGCHIPS = 1000
DISPLAYWIDTH = 70


class Session():
    """
    The Session object manages the general structure of a poker game. It sets up the essentials:
        game type, the table, and stakes.
    """
    def __init__(self, gametype, structure, tablesize=6, hero=None):
        """Initialize the poker Game."""

        self.blinds = structure
        self.rounds = 1
        self._table = setup_table.make(tablesize, hero)
        self._table.randomize_button()

        for p in self._table:
            p.chips = STARTINGCHIPS

    def __str__(self):
        """ Represents the game as the round # and the stakes level. """
        _str = 'Round: {:<5} '.format(self.rounds)
        stakes = 'Stakes: {}'.format(self.blinds)
        _str += stakes.rjust(43)

        return _str

    def play(self):
        """ Defines the structure of how a single hand in the poker game is played."""

        print('Stub play function')



class Round():
    def __init__(self, session):
        """
        Initialize the next round of Poker.
        """
        self._session = session
        self.street = 0
        self.pot = 0
        self.sidepots = {}
        self.betcap = 4
        self.betsize = 0
        self.level = 0
        self._table = session._table

        self.muck = []
        self.d = deck.Deck()
        self.DECKSIZE = len(self.d)

        # Create a list of the players from the table, and place the button at index 0
        self.bettor = None
        self.closer = None

        #  Remember starting stacks of all playerso
        self.betstack = {}
        self.startstack = {}
        for p in self._table:
            self.startstack[p.name] = p.chips

    def __str__(self):
        """ Show the current size of the pot. """
        _str = 'Pot: '
        _str += colors.color('${}'.format(self.pot), 'yellow')
        return _str.rjust(DISPLAYWIDTH)

    def deal_cards(self, qty, faceup=False):
        """
        Deal the specified quantity of cards to each player.
        """
        for i in range(qty):
            for p in self._table:
                c = self.d.deal()
                if faceup is True:
                    c.hidden = False
                p.add_card(c)

    def sortcards(self):
        for p in self._table:
            p._hand.sort()

    def muck_all_cards(self):
        """
        Fold all player hands and verify that the count of the muck matches the original
        deck size
        """
        # Clear hands
        for p in self._table:
            self.muck.extend(p.fold())
        # Add the remainder of the deck
        while len(self.d) > 0:
            self.muck.append(self.d.deal())

    def verify_muck(self):
        """ Verify that the integrity of the deck has not been compromised. """

        # Make sure that all cards have been used up.
        if len(self.d) != 0:
            return False
        # Check that the muck is the same size as the original starting deck.
        elif len(self.muck) != self.DECKSIZE:
            return False
        # Check that all players have folded.
        elif len(self._table.get_cardholders()) > 0:
            return False
        else:
            return True

    def post_antes(self):
        """ All players bet the ante amount and it's added to the pot. """
        for p in self._table:
            self.pot += p.bet(self._session.blinds.ANTE)

    def post_blinds(self):
        """
        Gets the small and big blind positions from the table and makes each player bet the
        appropriate mount to the pot. Returns a string describing what the blinds posted.
        """
        if self._table.TOKENS['D'] == -1:
            raise Exception('Button has not been set yet!')

        if len(self._table.get_players()) < 2:
            raise ValueError('Not enough players to play!')
            exit()
        sb = self._table.seats[self._table.TOKENS['SB']]
        bb = self._table.seats[self._table.TOKENS['BB']]

        # Bet the SB and BB amounts and add to the pot
        self.pot += sb.bet(self._session.blinds.SB)
        self.pot += bb.bet(self._session.blinds.BB)
        actions = ''
        actions += '{} posts ${}\n'.format(sb, self._session.blinds.SB)
        actions += '{} posts ${}\n'.format(bb, self._session.blinds.BB)
        return actions

    def setup_betting(self):
        """
        Set betsize, level, currentbettor and lastbettor.
        """
        # Preflop: Headsup
        if self.street == 0:
            # Preflop the first bettor is right after the BB
            self.level = 1
            self.betsize = self._session.blinds.BB
            self.closer = self._table.TOKENS['BB']
            self.bettor = self._table.next(self.closer)
            # Copy the starting stack for the first round (because blinds were posted)
            self.betstack = self.startstack.copy()

        elif self.street > 0:
            # postflop the first bettor is right after the button
            self.level = 0
            self.betsize = self._session.blinds.BB * 2

            self.bettor = self._table.next_player_w_cards(self._table.TOKENS['D'])
            before_button = (self._table.TOKENS['D'] - 1) % len(self._table)
            self.closer = self._table.next_player_w_cards(before_button)

            # Remember starting stack size.
            for p in self._table:
                self.betstack[p.name] = p.chips

    def get_stack_to_pot_list(self):
        """
        Returns a list of tuples. Each tuple is a stack and pot pair. The list get sorted
        by stacksize.
        """
        return sorted([(stack, self.sidepots[stack]) for stack in self.sidepots])

    def process_sidepots(self, handlist):
        """ Calculates which players are eligible to win which portions of the pot. Returns
        a dictionary of players and amounts. """
        # Organize the sidepots into an ascending sorted list.
        stacks_n_pots = self.get_stack_to_pot_list()

        leftovers = self.pot

        # Go through and process the main pot first,
        # then the 1st sidepot, 2nd sidepot, etc.
        for i, pot in enumerate(sorted(stacks_n_pots)):
            share = 0
            # Calculate the pot
            if i == 0:
                share = pot[1]
                leftovers -= pot[1]
            else:
                lastpot = stacks_n_pots[i - 1][1]
                share = pot[1] - lastpot
                leftovers -= share

            winners = self.eligible_for_pot(handlist, share, pot[0])
            print('Awarding ${} pot'.format(share))
            return self.split_pot(winners, share)

        if leftovers > 0:
            # We'll pass stacks_n_pots)[0] + 1 so that all the elibigle players are
            # just above the largest allin.
            above_allin = max(stacks_n_pots)[0] + 1
            winners = self.eligible_for_pot(handlist, leftovers, above_allin)
            print('Awarding ${} pot'.format(leftovers))
            return self.split_pot(winners, leftovers)

    def eligible_for_pot(self, handlist, pot, stack):
        """
        Determine what players are eligible to win pots and sidepots.
        """
        eligible = [p for p in handlist if self.startstack[p[1].name] >= stack]

        bestvalue = 0
        # Determine the best handvalue the eligible players have.
        for e in eligible:
            if e[0] > bestvalue:
                bestvalue = e[0]

        winners = [h[1] for h in eligible if h[0] == bestvalue]

        return winners

    def process_allins(self):
        """
        Determine which players are all-in in order to create sidepots.
        """
        for p in self._table.get_cardholders():
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
        if stacksize in self.sidepots:
            # There is already a sidepot for this stacksize
            return

        print('')
        mainpot = 0

        # Go through the table of players
        for p in self._table:
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

    def split_pot(self, winners, amt):
        """
        Adds the specified pot amount to the players chips.  If there are multiple winners,
        they must split the pot If there is a remainder amount, we give it to the next left of
        the BTN.  (ie: Usually the SB)
        """

        award_dict = {}
        if len(winners) > 1:
            share = int(amt / len(winners))
            remainder = amt % len(winners)
        else:
            share = amt
            remainder = 0

        for w in winners:
            award_dict[w] = share

        if remainder > 0:
            r_winner = self._table.seats[self._table.next(self._table.btn)]
            award_dict[r_winner] += remainder
        return award_dict

    def award_pot(self, player, amt):
        chips = colors.color('${}'.format(amt), 'yellow')
        print('\t{} wins {}'.format(player, chips))
        player.add_chips(amt)

    def betting_round(self):
        """
        Performs a round of betting between all the players that have cards and chips.
        """
        playing = True

        while playing:
            p = self._table.seats[self.bettor]
            invested = self.betstack[p.name] - p.chips
            cost = self.betsize * self.level - invested
            options = betting.get_options(cost, self)

            if p.chips == 0:
                print('{} is all in.'.format(p))
            elif p.playertype == 'HUMAN':
                print(self)
                o = betting.menu(options)
                #  action_string = self.process_option(o)
            else:
                o = strategy.makeplay(p, self, options)
                #  action_string = self.process_option(o)
            action_string = self.process_option(o)
            print(action_string)

            if self._table.valid_bettors() == 1:
                print('Only one player left!')
                winner = self._table.seats[self._table.next_player_w_cards(self.bettor)]
                self.PLAYING = False
                # Return the single winner as a list so award_pot can use it.
                return [winner]

            elif self.bettor == self.closer:
                # Reached the last bettor, betting is closed.
                playing = False
            else:
                # Set next bettor
                self.bettor = self._table.next_player_w_cards(self.bettor)

        else:
            # The betting round is over, and there are multiple players still remaining.
            self.street += 1
            return None

    def process_option(self, option):
        """ Performs the option picked by a player. """
        p = self._table.seats[self.bettor]

        if option[0] == 'FOLD':
            self.muck.extend(p.fold())

        elif option[2] > 0:
            # It's a raise, so we'll need to reset last better.
            self.closer = self._table.next_player_w_cards(self.bettor, -1)
            self.pot += p.bet(option[1])
            self.level += option[2]
        else:
            self.pot += p.bet(option[1])

        act_str = ''
        act_str += '  ' * self.level
        act_str += '{} {}s'.format(p, option[0].lower())

        amt = colors.color(' $' + str(option[1]), 'yellow')

        if option[0] in ['BET', 'RAISE']:
            return colors.color(act_str, 'red') + amt
        elif option[0] in ['FOLD', 'CHECK']:
            return colors.color(act_str, 'purple')
        else:
            return colors.color(act_str, 'white') + amt

    def showdown(self):
        """
        Compare all the hands of players holding cards and determine the winner(s).
        Return a dictionary of players and the amounts they will be awarded.
        """
        for p in self._table.get_cardholders():
            p.showhand()
            print('{:15} shows: {}: {}, {}'.format(
                str(p), p._hand, p._hand.handrank, p._hand.description))

        handlist = self._table.get_valuelist()
        self.process_allins()

        if len(self.sidepots) == 0:
            # No sidepots, so the minimum for elibility is 0.
            winners = self.eligible_for_pot(handlist, self.pot, 0)
            return self.split_pot(winners, self.pot)

        else:
            return self.process_sidepots(handlist)
