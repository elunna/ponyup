from __future__ import print_function
import betting
import blinds as b
import colors
import deck
import testtools

DISPLAYWIDTH = 70

STREETS = {
    'OMAHA': [1, 1, 2, 2],
    'HOLDEM': [1, 1, 2, 2],
    'FIVE CARD DRAW': [1, 2],
    'FIVE CARD STUD': [1, 1, 2, 2],
    'SEVEN CARD STUD': [1, 1, 2, 2, 2],
}


class Session():
    """
    The Session object manages the general structure of a poker game. It sets up the essentials:
        game type, the table, and stakes.
    """
    def __init__(self, gametype, blinds=None, tablesize=None, hero=None):
        """
        Initialize the poker Session settings.
        """
        self.gametype = gametype
        self.rounds = 1
        self._table = testtools.make(tablesize, hero)
        self._table.randomize_button()

        self.streets = STREETS[gametype]
        if blinds is None:
            self.blinds = b.Blinds()
        else:
            self.blinds = blinds

    def __str__(self):
        """
        Returns the Session info.
        """
        _str = 'Round: {:<5}\n'.format(self.rounds)
        stakes = 'Stakes: {}'.format(self.blinds)
        _str += stakes.rjust(DISPLAYWIDTH)

        return _str

    def new_round(self):
        return Round(self)

    def play(self):
        """
        Defines the structure of how a single hand in the poker game is played.
        """
        print('Stub play function')


class Round():
    def __init__(self, session):
        """
        Initialize the next round of Poker.
        """
        self.blinds = session.blinds
        self.street = 0
        self.streets = session.streets
        self.pot = 0
        self.sidepots = {}
        self._table = session._table

        self.muck = []
        self.d = deck.Deck()
        self.DECKSIZE = len(self.d)

        #  Remember starting stacks of all players
        self.starting_stacks = self._table.stackdict()

    def __str__(self):
        """
        Return info about the current round.
        """
        _str = 'Pot: '
        _str += colors.color('${}'.format(self.pot), 'yellow')
        return _str.rjust(84)

    def deal_cards(self, qty, faceup=False):
        """
        Deal the specified quantity of cards to each player. If faceup is True, the cards are
        dealt face-up, otherwise they are face-down.
        """
        for i in range(qty):
            for p in self._table:
                c = self.d.deal()
                if faceup is True:
                    c.hidden = False
                p.add_card(c)

    def show_cards(self):
        """
        Unhides all player hands and returns a string that shows all the player hands.
        """
        _str = ''
        for p in self._table.get_players(CARDS=True):
            p.showhand()
            line = '\t\t\t\t {:>15} shows {:10}\n'.format(str(p), str(p._hand))
            _str += line
        return _str

    def sortcards(self):
        """
        Sort all cards in all players hands.
        """
        for p in self._table:
            p._hand.sort()

    def muck_all_cards(self):
        """
        Muck all player hands, and muck the contents of the deck.
        """
        # Clear hands
        for p in self._table:
            self.muck.extend(p.fold())
        # Add the remainder of the deck
        while len(self.d) > 0:
            self.muck.append(self.d.deal())

    def post_antes(self):
        """
        All players bet the ante amount and it's added to the pot.
        """
        for p in self._table:
            self.pot += p.bet(self.blinds.ANTE)

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
        self.pot += sb.bet(self.blinds.SB)
        self.pot += bb.bet(self.blinds.BB)
        actions = ''
        actions += '{} posts ${}\n'.format(sb, self.blinds.SB)
        actions += '{} posts ${}\n'.format(bb, self.blinds.BB)
        return actions

    def invested(self, player):
        """
        Return the difference between the players current stack-size and the amount at the
        start of the round.
        """
        return self.starting_stacks[player.name] - player.chips

    def get_allins(self):
        """
        Returns a list of all stack sizes that went all-in this round.
        """
        return [self.starting_stacks[p.name] for p in self._table.get_players(CARDS=True)
                if p.is_allin()]

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
        return [p for p in eligible_players if p._hand.value() == best_hand]

    def best_hand_val(self, players):
        """
        Determine the best handvalue within the given player group.
        """
        best = 0
        for p in players:
            if p._hand.value() > best:
                best = p._hand.value()
        return best

    def get_eligible(self, stack_req):
        """
        Returns a list of players who had the minimum starting stack size.
        """
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
            first_after_btn = self._table.next_player(self._table.btn)
            r_winner = self._table.seats[first_after_btn]
            award_dict[r_winner] += remainder
        return award_dict

    def betting_round(self):
        """
        Run through a round of betting. Returns a victor if it exists.
        """
        br = betting.BettingRound(self)
        victor = br.play()
        self.street += 1
        return victor

    def showdown(self):
        """
        Compare all the hands of players holding cards and determine the winner(s). Awards each
        winner the appropriate amount.
        """
        print(self.show_cards())

        allins = self.get_allins()
        sidepots = self.make_sidepots(allins)
        # Return the award_dict
        self.process_awards(self.process_sidepots(sidepots))

    def process_awards(self, award_dict):
        """
        Takes in the dictionary of awards/players and awards each player their share. Uses
        split pot to correctly split up ties.
        """
        for sidepot, winners in award_dict.items():
            for p, s in self.split_pot(winners, sidepot).items():

                h_txt = '{:>15} wins with a {}: {}'.format(
                    str(p),
                    str(p._hand.rank()),
                    str(p._hand.desc())
                )
                print(h_txt.strip().rjust(70))
                self.award_pot(p, s)

    def award_pot(self, player, amt):
        """
        Adds the specified amount to a players stack.
        """
        chips = colors.color('${}'.format(amt), 'yellow')
        w_txt = '{:>15} wins {}'.format(str(player), chips)
        txt = w_txt.strip().rjust(84)
        print(txt)
        player.add_chips(amt)

    def next_street(self):
        """
        Advanced the street counter by one.
        """
        if self.street >= len(self.streets):
            raise Exception('The last street has been reached on this game!')
        else:
            self.street += 1

    def check_integrity_post(self):
        """
        Verify that the game elements have been cleaned up correctly and that all cards are
        accounted for.
        """
        # Check that all cards have been used up.
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
