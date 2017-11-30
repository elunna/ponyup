"""
  " Tools for managing a betting round - the betsize, the max raise, order of betting, etc.
  """
from collections import namedtuple
from ponyup import strategy

Action = namedtuple('Action', ['name', 'cost'])
ALLIN = Action('ALLIN', 0)
CHECK = Action('CHECK', 0)
FOLD = Action('FOLD', 0)


class BettingRound(object):
    """ Manages the betting info and activities."""
    def __init__(self, r):
        self.stacks = None
        self.closer = None
        self.betsize = None

        self.pot = r.pot
        self.r = r
        self.BETCAP = 4
        self.bettor = self.get_utg()
        self.set_closer()
        self.set_betsize()
        self.set_stacks()

        # We cannot set the current_bet until stacks have been set!
        self.bet = self.get_bet()

        # Create the generator
        self.play_generator = self.__iter__()

    def __getattr__(self, name):
        try:
            return getattr(self.r, name)
        except AttributeError:
            raise AttributeError("Child' object has no attribute {}".format(name))

    def __iter__(self):
        """ This is a generator which yields the next betting player on a betting
            round. When all the bettors have been exhausted or everybody has
            folded except for one player, then the generator stops.
        """
        while True:
            yield self.get_bettor()

            if self.one_left() or self.done():
                raise StopIteration()
            else:
                self.next_bettor()

    def __next__(self):
        return next(self.play_generator)

    def cpu_decision(self, s):
        """ Presents the current bettor with their options and lets them pick one.
            Returns the Action object they picked.
        """
        options = self.get_options(s)

        if 'a' in options:
            # Player is allin
            return Action('ALLIN', 0)
        else:
            facing = self.cost(s) / self.betsize
            return strategy.makeplay(s, options, self.street, self.level(), facing)

    def process_option(self, action):
        """ Performs the option picked by a player.  """
        s = self.get_bettor()

        if action.name == 'FOLD':
            self.muck.extend(s.fold())
            return
        elif action.name in ['CHECK', 'ALLIN']:
            return
        elif action.name in ['BET', 'RAISE']:
            # We follow the half-bet rule: If an allin bet or raise is equal to or larger than
            # half the minimum bet amount, it does constitute a real raise and reopens the
            # betting.
            # A player can also "complete" an incomplete bet or raise, and this would reopen the
            # betting as well.

            # Double check amount:
            if self.level() == 0 and action.cost > self.betsize:
                raise Exception('Bet amount is more than the opening size! {} vs {}'.format(
                    action.cost, self.betsize))

            # Reset the closer anytime the betting is reopened.
            self.closer = self.reopened_closer(self.bettor)

        # If the bet amount is over the ongoing bet amount - reset the bet amount.
        player_bet = action.cost + self.invested(s)
        if player_bet > self.bet:
            self.bet = player_bet

        # Add the bet/raise amount to the pot
        self.pot += s.bet(action.cost)

    def get_options(self, s):
        """ Shows the options available to the current bettor.  """
        cost = self.cost(s)
        stack = s.stack
        option_dict = {}
        #  completing = (self.betsize - cost) == self.blinds.SB

        if stack == 0:
            option_dict['a'] = ALLIN
            return option_dict

        if cost == 0:
            option_dict['c'] = CHECK

        elif cost > 0:
            option_dict['f'] = FOLD

            if stack >= cost:
                option_dict['c'] = Action('CALL', cost)
            else:
                # Player doesn't have enough for the full call amount
                option_dict['c'] = Action('CALL', stack)

        minraise_amt = self.betsize * self.level() + (self.betsize / 2)
        minraise_cost = minraise_amt - self.invested(s)

        raise_amt = (self.betsize * self.level() + self.betsize)
        raise_cost = raise_amt - self.invested(s)
        bet_cost = self.betsize - self.invested(s)

        if self.level() == 0:
            if bet_cost > 0:
                # "Completing" the bringin
                option_dict['b'] = Action('BET', bet_cost)
            elif stack >= self.betsize:
                option_dict['b'] = Action('BET', self.betsize)
            else:
                option_dict['b'] = Action('BET', stack)  # Allin bet

        if self.level() >= 1 and self.level() < self.BETCAP:
            if stack < minraise_cost:
                # They don't qualify for a full raise - it's a bet instead.
                option_dict['b'] = Action('BET', stack)  # Allin bet

            #  elif self.bet < minraise_amt and stack >= raise_cost:
                # The current bet cannot be raised, it can be completed with a BET.
                #  option_dict['b'] = Action('BET', raise_cost)

            elif stack >= raise_cost:
                # They can cover the full cost of the raise.
                option_dict['r'] = Action('RAISE', raise_cost)
            else:
                # Player doesn't have enough for a full raise, but enough for a partial raise.
                option_dict['r'] = Action('RAISE', stack)

        return option_dict

    def action_string(self, action):
        s = self.get_bettor()
        act_str = []
        act_str.append('{} {}s '.format(s.player, action.name.lower()))

        if action.name in ['CALL', 'BET', 'RAISE']:
            act_str.append('${}'.format(str(action.cost)))
            return act_str
        elif action.name in ['FOLD', 'CHECK']:
            return act_str
        elif action.name == 'ALLIN':
            return ['{} is all in.'.format(s.player)]
        else:
            raise Exception('Error processing the action!')

    def invested(self, seat):
        # Adjust for antes posted. Antes should NOT be counted in the bet amounts.
        # This only counts for the 1st street, when antes are posted.
        if self.street == 0:
            return (self.stacks[seat.NUM] - seat.stack) - self.blinds.ANTE
        else:
            return self.stacks[seat.NUM] - seat.stack

        #  return self.stacks[player.name] - player.chips

    def cost(self, p):
        return self.bet - self.invested(p)

    def done(self):
        return self.bettor == self.closer

    def set_closer(self):
        self.closer = self.table.next_player(self.bettor, -1, hascards=True)

    def set_betsize(self):
        if self.street > len(self.streets):
            raise Exception('The street is larger than the number of streets in the game!')
        else:
            self.betsize = self.get_street().betsize * self.blinds.SMBET

    def get_bet(self):
        """ Returns how much the current player has to pay  """
        bet = 0
        for s in self.table:
            i = self.invested(s)
            if i > bet:
                bet = i
        # Adjust for ante.
        #  if self.street == 0:
            #  bet - self.blinds.ANTE
        return bet

    def level(self):
        return int(self.bet // self.betsize)

    def get_bettor(self):
        """
        Returns the current active bettor.
        """
        return self.table.seats[self.bettor]

    def next_bettor(self):
        self.bettor = self.table.next_player(self.bettor, hascards=True)

    def get_closer(self):
        """
        Returns the player who will close the betting.
        """
        return self.table.seats[self.closer]

    def reopened_closer(self, bettor):
        # It's a bet or raise, so we'll need to reset last better.
        return self.table.next_player(bettor, -1, hascards=True)

    def set_stacks(self):
        if self.street == 0:
            self.stacks = self.pot.stacks
        elif self.street > 0:
            self.stacks = self.table.stackdict()

    def betmenu(self, actions):
        """ Return a string showing the betting options.  """
        nice_opts = ['[' + v.name[0] + ']' + v.name[1:].lower() for v in sorted(actions.values())]
        choices = '/'.join(nice_opts)
        return choices


def spacing(level):
    """ Spaces the player actions by the current bet level.  """
    return '   ' * level
