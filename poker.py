from __future__ import print_function
import betting
import colors
import deck
import setup_table
import stacks
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
        _str = 'Round: {:<5}\n'.format(self.rounds)
        stakes = 'Stakes: {}'.format(self.blinds)
        _str += stakes.rjust(DISPLAYWIDTH)

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
        self.starting_stacks = stacks.stackdict(self._table)

    def __str__(self):
        """ Show the current size of the pot. """
        _str = 'Pot: '
        _str += colors.color('${}'.format(self.pot), 'yellow')
        return _str.rjust(84)

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

    def show_cards(self):
        _str = ''
        for p in self._table.get_players(CARDS=True):
            p.showhand()
            line = '\t\t\t\t {:>15} shows {:10}\n'.format(str(p), str(p._hand))
            _str += line
        return _str

    def sortcards(self):
        for p in self._table:
            p._hand.sort()

    def muck_all_cards(self):
        """ Muck all player hands, and muck the contents of the deck. """
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
        elif len(self._table.get_players(CARDS=True)) > 0:
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

    def get_valuelist(self):
        """
        Find all players with cards; return a list of hand values and player objects.
        """
        return [(p._hand.value, p) for p in self._table.get_players(CARDS=True)]

    def valuelist2(self):
        """ Find all the players with cards and return a list of hand values. """
        return [p._hand.value for p in self._table.get_players(hascards=True)]

    def invested(self, player):
        return self.starting_stacks[player.name] - player.chips

    def get_allins(self):
        """ Returns a list of all stack sizes that went all in this round."""
        return [self.starting_stacks[p.name] for p in self._table.get_players(CARDS=True)
                if p.is_allin()]

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
            self.betstack = self.starting_stacks.copy()

        elif self.street > 0:
            # postflop the first bettor is right after the button
            self.level = 0
            self.betsize = self._session.blinds.BB * 2

            self.bettor = self._table.next_player_w_cards(self._table.TOKENS['D'])
            before_button = (self._table.TOKENS['D'] - 1) % len(self._table)
            self.closer = self._table.next_player_w_cards(before_button)

            # Remember starting stack size.
            self.betstack = stacks.stackdict(self._table)

    def make_sidepots(self, allins):
        """
        Sidepot is how much the given stack size(s) can win.  Takes in a list of all-in
        stack-size amounts and returns a dictionary of pot:stacksize pairs that show what
        sidepots are available and what stack size is required to win it.
        """
        POTS = {}

        for stacksize in allins:
            if stacksize in POTS:
                continue

            sidepot = 0
            for p in self._table:
                # Get the players total invested amount over the round
                i = self.invested(p)

                # If stacksize is less than invested, they can only win the stacksize.
                if stacksize <= i:
                    sidepot += stacksize
                elif stacksize > i:
                    # if their stacksize is more than invested, they can win the entire invested
                    # amount.
                    sidepot += i

            # Adjust the sidepot
            # The sidepot is what is leftover after taking off the next-lesser sidepot.
            if len(POTS) == 0:
                POTS[stacksize] = sidepot
            else:
                #  last_sidepot = POTS[max(POTS)]
                POTS[stacksize] = sidepot - sum(POTS.values())
        return POTS

    def process_sidepots(self, sidepots):
        """
        Calculates which players are eligible to win which portions of the pot.
        Returns a dictionary of pot shares and player lists.
        """
        leftovers = self.pot
        shares = {}
        if len(sidepots) == 0:
            required_stack = 0
        else:
            required_stack = max(sidepots) + 1

        while len(sidepots) > 0:
            stack = min(sidepots)
            share = sidepots[stack]
            leftovers -= share
            shares[share] = self.eligible_for_pot(stack)
            sidepots.pop(stack)

        if leftovers > 0:
            # The above_allin variable lets anyone above the allin threshold win the leftovers.
            shares[leftovers] = self.eligible_for_pot(required_stack)
        return shares

    def eligible_for_pot(self, stack_required):
        """
        Makes a list of the players who qualify the given stack size and who have (or tie) the
        best hand of all cardholding players.
        """
        eligible_players = self.get_eligible(stack_required)
        best_hand = self.best_hand_val(eligible_players)
        return [p for p in eligible_players if p._hand.value == best_hand]

    def best_hand_val(self, players):
        """ Determine the best handvalue within the givenplayer group. """
        best = 0
        for p in players:
            if p._hand.value > best:
                best = p._hand.value
        return best

    def get_eligible(self, stack_req):
        """ Returns a list of players who had the minimum starting stack size. """
        cardholders = self._table.get_players(CARDS=True)
        return [p for p in cardholders if self.starting_stacks[p.name] >= stack_req]

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
            first_after_btn = self._table.next(self._table.btn)
            r_winner = self._table.seats[first_after_btn]
            award_dict[r_winner] += remainder
        return award_dict

    def betting_round(self):
        """
        Performs a round of betting between all the players that have cards and chips.
        """
        playing = True

        while playing:
            p = self._table.seats[self.bettor]
            invested = self.betstack[p.name] - p.chips
            cost = (self.betsize * self.level) - invested
            options = betting.get_options(cost, self)

            if p.is_allin():
                o = betting.allin_option()
            elif p.playertype == 'HUMAN':
                print(self)
                o = betting.menu(options)
            else:
                o = strategy.makeplay(p, self, options)

            action_string = betting.process_option(o, self)
            print(action_string)

            #  if self._table.valid_bettors() == 1:
            cardholders = self._table.get_players(CARDS=True)
            if len(cardholders) == 1:
                oneleft = '{}Only one player left!'.format(betting.spacing(self.level))
                print(colors.color(oneleft, 'LIGHTBLUE'))
                #  winner = self._table.seats[self._table.next_player_w_cards(self.bettor)]
                #  winner =
                # Return the single winner as a list so award_pot can use it.
                return cardholders

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

    def showdown(self):
        """
        Compare all the hands of players holding cards and determine the winner(s).
        Return a dictionary of players and the amounts they will be awarded.
        """
        print(self.show_cards())

        allins = self.get_allins()
        sidepots = self.make_sidepots(allins)
        # Return the award_dict
        return self.process_sidepots(sidepots)

    def process_awards(self, award_dict):
        for sidepot, winners in award_dict.items():
            for p, s in self.split_pot(winners, sidepot).items():
                self.award_pot(p, s)

    def award_pot(self, player, amt):
        h_txt = '{:>15} wins with a {}: {}'.format(str(player), str(player._hand.handrank),
                                                   str(player._hand.description))
        chips = colors.color('${}'.format(amt), 'yellow')
        w_txt = '{:>15} wins {}'.format(str(player), chips)
        txt = h_txt.strip().rjust(70)
        txt += '\n'
        txt += w_txt.strip().rjust(84)
        print(txt)
        player.add_chips(amt)
