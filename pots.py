class Pot():
    def __init__(self, table):
        self.pot = 0
        self.table = table
        #  Remember starting stacks of all players
        self.stacks = table.stackdict()

    def __add__(self, other):
        return self.pot + other

    def __iadd__(self, other):
        self.pot += other
        return self

    def __eq__(self, other):
        return self.pot == other

    def __str__(self):
        return str(self.pot)

    def invested(self, seat):
        """
        Returns how much the seat has invested over the entire round.
        """
        return self.stacks[seat.NUM] - seat.stack

    def allin_stacks(self):
        broke_seats = self.table.get_broke_players()
        return [self.stacks[s.NUM] for s in broke_seats]

    def make_sidepots(self):
        """
        Sidepot is how much the given stack size(s) can win.  Takes in a list of all-in
        stack-size amounts and returns a dictionary of pot:stacksize pairs that show what
        sidepots are available and what stack size is required to win it.
        """
        POTS = {}

        for stacksize in sorted(self.allin_stacks()):
            if stacksize in POTS:
                continue

            sidepot = self.calc_sidepot(stacksize)
            # Adjust the sidepot
            # The sidepot is what is leftover after taking off the next-lesser sidepot.
            if len(POTS) == 0:
                POTS[stacksize] = sidepot
            else:
                #  last_sidepot = POTS[max(POTS)]
                POTS[stacksize] = sidepot - sum(POTS.values())
        return POTS

    def calc_sidepot(self, stacksize):
        """
        Calculates the maximum value a stacksize can win from the current pot.
        """
        sidepot = 0
        for s in self.table:
            # Get the players total invested amount over the round
            i = self.invested(s)

            # If stacksize is less than invested, they can only win the stacksize.
            if stacksize <= i:
                sidepot += stacksize
            elif stacksize > i:
                # if their stacksize is more than invested, they can win the entire invested
                # amount.
                sidepot += i
        return sidepot

    def process_sidepots(self, sidepots):
        """
        Calculates which players are eligible to win which portions of the pot.
        Returns a dictionary of pot shares and player lists.
        """
        leftovers = self.pot
        shares = {}
        # If there are no sidepots, then there is no stacksize requirement to win the main pot.
        if len(sidepots) == 0:
            required_stack = 0
        else:
            required_stack = max(sidepots) + 1

        while len(sidepots) > 0:
            # Work up from the lowest stack to the highest.
            stack = min(sidepots)
            pot = sidepots[stack]
            leftovers -= pot

            # Determine which players can win this share of the pot.
            shares[pot] = self.eligible_for_pot(stack)

            # Move onto the next sidepot.
            sidepots.pop(stack)

        # Award what is leftover after the sidepots.
        if leftovers > 0:
            # required_stack lets anyone above the allin threshold win the leftovers.
            shares[leftovers] = self.eligible_for_pot(required_stack)
        return shares

    def get_eligible(self, stack_req):
        """
        Returns a list of seats that have the minimum starting stack size.
        """
        cardholders = self.table.get_players(hascards=True)
        return [s for s in cardholders if self.stacks[s.NUM] >= stack_req]

    def eligible_for_pot(self, stack_required):
        """
        Makes a list of the players who qualify the given stack size and who have (or tie) the
        best hand of all cardholding players.
        """
        eligible_players = self.get_eligible(stack_required)
        best_hand = best_hand_val(eligible_players)
        return [s.NUM for s in eligible_players if s.hand.value() == best_hand]

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
            first_after_btn = self.table.next_player(self.table.btn, hascards=True)
            r_winner = self.table.seats[first_after_btn].NUM
            award_dict[r_winner] += remainder
        return award_dict

    def process_awards(self, award_dict):
        """
        Takes in the dictionary of awards/seats and awards each player their share. Uses
        split pot to correctly split up ties.
        """
        _str = ''
        for sidepot, winners in award_dict.items():
            for i, amt in self.split_pot(winners, sidepot).items():
                seat = self.table.seats[i]
                _str += '{} wins with a {}: {}\n'.format(
                    str(seat.player),
                    str(seat.hand.rank()),
                    str(seat.hand.desc())
                )
                _str += award_pot(seat, amt)
        return _str

    def valid_sidepots(self, sidepots):
        """
        Verifies that all sidepots add up to the current pot amount. If the sum of the sidepots
        equals the pot, returns True. Otherwise returns False.
        """
        total = 0
        for s in sidepots:
            total += s
        if total != self.pot:
            return False
        else:
            return True

    def allocate_money_to_winners(self):
        stack_shares = self.make_sidepots()
        sidepots = self.process_sidepots(stack_shares)

        if not self.valid_sidepots(sidepots):
            raise Exception('Sidepots are not valid - they do not total the pot amount!')

        if len(sidepots) > 1:
            for i, s in enumerate(sidepots):
                self.log('Sidepot #{}: ${}'.format(i+1, s))

        award_txt = self.process_awards(sidepots)
        return award_txt


###########################
# Independent Functions
def award_pot(seat, amt):
    """
    Adds the specified amount to a players stack. Returns a string describing who won what.
    """
    if seat.has_hand():
        seat.win(amt)
        return '{:} wins ${}\n'.format(str(seat.player), amt)
    else:
        raise ValueError('Player has no hand! Not eligible to win any pot!')


def best_hand_val(seats):
    """
    Determine the best handvalue within the given group of seats.
    """
    best = 0
    for s in seats:
        if s.hand.value() > best:
            best = s.hand.value()
    return best


def calc_odds(bet, pot):
    """
    Calculate the odds offered to a player given a bet amount and a pot amount.
    """
    if bet < 0 or pot < 0:
        raise ValueError('bet or pot must be positive!')
    odds = pot / bet
    return odds
