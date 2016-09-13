from __future__ import print_function
from collections import namedtuple
import console
import strategy
import stud

Action = namedtuple('Action', ['name', 'cost'])
ALLIN = Action('ALLIN', 0)
CHECK = Action('CHECK', 0)
FOLD = Action('FOLD', 0)


class BettingRound():
    def __init__(self, r):
        """
        Manages the betting info and activities. Takes in a Round object as r.
        """
        self.pot = r.pot
        self.r = r
        self.BETCAP = 4
        if self.r.gametype == "FIVE CARD DRAW":
            self.set_bettors_w_blinds()
        elif self.r.gametype in ["FIVE CARD STUD", "SEVEN CARD STUD"]:
            self.set_bettors_w_antes()

        self.set_betsize()
        self.set_stacks()

        # We cannot set the current_bet until stacks have been set!
        self.bet = self.get_bet()

        # Create the generator
        self.play_generator = self.__iter__()

    def __iter__(self):
        """
        This is a generator which yields the next betting player on a betting round. When all
        the bettors have been exhausted or everybody has folded except for one player, then
        the generator stops.
        """
        while True:
            yield self.get_bettor()

            if self.r.one_left() or self.done():
                raise StopIteration()
            else:
                self.next_bettor()

    def __next__(self):
        return next(self.play_generator)

    def player_decision(self, s):
        """
        Takes in a player p and calculates the cost of the current minimum bet amount for that
        player, based on how much they have invested so far this round. It takes that cost and
        passes it to get_options to determine what betting options the player has.

        The next step depends on whether the player is human, or computer, or if they are all-
        in then they don't have a decision and the betting passes to the next player. If human,
        they are prompted for their decision. If CPU, they follow an algorithm for making a
        play. The decision is returned as an Action object.
        """
        options = self.get_options(s)

        if 'a' in options:
            # Player is allin
            return Action('ALLIN', 0)
        elif s.player.is_human():
            return console.betmenu(options)
        else:
            facing = self.cost(s) / self.betsize
            return strategy.makeplay(s, options, self.r.street, self.level(), facing)

    def process_option(self, action):
        """
        Performs the option picked by a player.
        """
        s = self.get_bettor()

        if action.name == 'FOLD':
            self.r.muck.extend(s.fold())
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
        """
        Shows the options available to the current bettor.
        """
        cost = self.cost(s)
        stack = s.stack
        option_dict = {}
        #  completing = (self.betsize - cost) == self.r.blinds.SB

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
        act_str = ''
        act_str += '{} {}s'.format(s.player, action.name.lower())

        if action.name in ['CALL', 'BET', 'RAISE']:
            return '{} ${}'.format(act_str, str(action.cost))
        elif action.name in ['FOLD', 'CHECK']:
            return act_str
        elif action.name == 'ALLIN':
            return '{} is all in.'.format(s.player)
        else:
            raise Exception('Error processing the action!')

    def invested(self, seat):
        # Adjust for antes posted. Antes should NOT be counted in the bet amounts.
        # This only counts for the 1st street, when antes are posted.
        if self.r.street == 0:
            return (self.stacks[seat.NUM] - seat.stack) - self.r.blinds.ANTE
        else:
            return self.stacks[seat.NUM] - seat.stack

        #  return self.stacks[player.name] - player.chips

    def cost(self, p):
        return self.bet - self.invested(p)

    def done(self):
        return self.bettor == self.closer

    def set_bettors_w_blinds(self):
        if self.r._table.TOKENS['D'] == -1:
            raise Exception('Cannot set bettor or closer in the if button isn\'t set!')
        if self.r.street == 0:
            self.closer = self.r._table.TOKENS['BB']
            self.bettor = self.r._table.next_player(self.closer)
        else:
            self.bettor = self.r._table.next_player(self.r._table.TOKENS['D'], hascards=True)
            self.closer = self.r._table.next_player(self.bettor, -1, hascards=True)

    def set_bettors_w_antes(self):
        if self.r.street == 0:
            self.bettor = stud.bringin(self.r._table)
            self.closer = self.r._table.next_player(self.bettor, -1, hascards=True)
        else:
            # Go with high-hand
            # Default to lowest seat #, change this later.
            self.bettor = stud.highhand(self.r._table, self.r.gametype)
            self.closer = self.r._table.next_player(self.bettor, -1, hascards=True)

    def set_betsize(self):
        if self.r.street > len(self.r.streets):
            raise Exception('The street is larger than the number of streets in the game!')
        else:
            self.betsize = self.r.get_street().betsize * self.r.blinds.BB

    def get_bet(self):
        bet = 0
        for s in self.r._table:
            i = self.invested(s)
            if i > bet:
                bet = i
        # Adjust for ante.
        #  if self.r.street == 0:
            #  bet - self.r.blinds.ANTE
        return bet

    def level(self):
        return int(self.bet // self.betsize)

    def get_bettor(self):
        """
        Returns the current active bettor.
        """
        return self.r._table.seats[self.bettor]

    def next_bettor(self):
        self.bettor = self.r._table.next_player(self.bettor, hascards=True)

    def get_closer(self):
        """
        Returns the player who will close the betting.
        """
        return self.r._table.seats[self.closer]

    def reopened_closer(self, bettor):
        # It's a bet or raise, so we'll need to reset last better.
        return self.r._table.next_player(bettor, -1, hascards=True)

    def set_stacks(self):
        if self.r.street == 0:
            self.stacks = self.pot.stacks
        elif self.r.street > 0:
            self.stacks = self.r._table.stackdict()


def spacing(level):
    """
    Spaces the player actions by the current bet level.
    """
    return '  ' * level
