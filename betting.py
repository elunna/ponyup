from __future__ import print_function
from collections import namedtuple
import colors
import strategy
import poker

Action = namedtuple('Action', ['name', 'cost'])
ALLIN = Action('ALLIN', 0)
CHECK = Action('CHECK', 0)
FOLD = Action('FOLD', 0)


class BettingRound():
    def __init__(self, r):
        """
        Manages the betting info and activities. Takes in a Round object as r.
        """
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

    def play(self):
        """
        This is a generator which yields the next betting player on a betting round. When all
        the bettors have been exhausted or everybody has folded except for one player, then
        the generator stops.
        """
        while True:
            yield self.get_bettor()

            if one_left(self.r._table) or self.done():
                raise StopIteration()
            else:
                self.next_bettor()

    def player_decision(self, p):
        """
        Takes in a player p and calculates the cost of the current minimum bet amount for that
        player, based on how much they have invested so far this round. It takes that cost and
        passes it to get_options to determine what betting options the player has.

        The next step depends on whether the player is human, or computer, or if they are all-
        in then they don't have a decision and the betting passes to the next player. If human,
        they are prompted for their decision. If CPU, they follow an algorithm for making a
        play. The decision is returned as an Action object.
        """
        invested = self.invested(p)
        cost = self.cost(invested)
        #  cost = (self.betsize * self.level) - invested
        options = self.get_options(cost, p.chips)

        if 'a' in options:
            # Player is allin
            return Action('ALLIN', 0)
        elif p.is_human():
            return menu(options)
        else:
            facing = cost / self.betsize
            return strategy.makeplay(p, options, self.r.street, self.get_betlevel(), facing)

    def process_option(self, action):
        """
        Performs the option picked by a player.
        """
        p = self.get_bettor()

        if action.name == 'FOLD':
            self.r.muck.extend(p.fold())
            return
        elif action.name in ['CHECK', 'ALLIN']:
            return
        elif action.name == 'BET':
            # We follow the half-bet rule: If an allin bet or raise is equal to or larger than
            # half the minimum bet amount, it does constitute a real raise and reopens the
            # betting.
            # A player can also "complete" an incomplete bet or raise, and this would reopen the
            # betting as well.

            # Double check amount:
            if self.get_betlevel() == 0 and action.cost > self.betsize:
                raise Exception('Bet amount is more than the opening size! {} vs {}'.format(
                    action.cost, self.betsize))

            minimum_bet = self.betsize / 2
            if action.cost >= minimum_bet:
                self.closer = self.reopened_closer(self.bettor)

        elif action.name == 'RAISE':
            minimum_raise = (self.betsize * self.get_betlevel()) + (self.betsize / 2)
            if action.cost >= minimum_raise:
                self.closer = self.reopened_closer(self.bettor)

        # If the bet amount is over the ongoing bet amount - reset the bet amount.
        player_bet = action.cost + self.invested(p)
        if player_bet > self.bet:
            self.bet = player_bet

        # Add the bet/raise amount to the pot
        self.r.pot += p.bet(action.cost)

    def get_options(self, cost, stack):
        """
        Shows the options available to the current bettor.
        """
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

        minimum_raise = (self.betsize * self.get_betlevel()) + (self.betsize / 2)
        raise_cost = (self.betsize * self.get_betlevel()) + self.betsize

        if self.get_betlevel() == 0:
            # Player doesn't have enough for the full bet amount
            if stack >= self.betsize:
                option_dict['b'] = Action('BET', self.betsize)
            else:
                option_dict['b'] = Action('BET', stack)

        if self.get_betlevel() >= 1 and self.get_betlevel() < self.BETCAP:

            if stack < self.betsize:
                # Player does not have enough chips for a raise.
                pass
            elif stack >= self.betsize * self.get_betlevel() and stack < minimum_raise:
                # They don't qualify for a full raise - it's a bet instead.
                option_dict['b'] = Action('BET', stack)

            elif stack >= raise_cost:
                option_dict['r'] = Action('RAISE', raise_cost)
            else:
                # Player doesn't have enough for a full raise, but enough for a partial raise.
                option_dict['r'] = Action('RAISE', stack)

        return option_dict

    def action_string(self, action):
        p = self.get_bettor()
        act_str = ''
        act_str += spacing(self.get_betlevel())
        act_str += '{} {}s'.format(p, action.name.lower())

        amt = colors.color(' $' + str(action.cost), 'yellow')

        if action.name in ['BET', 'RAISE']:
            return colors.color(act_str, 'red') + amt
        elif action.name == 'CALL':
            return colors.color(act_str, 'white') + amt
        elif action.name == 'FOLD':
            return colors.color(act_str, 'purple')
        elif action.name == 'CHECK':
            return colors.color(act_str, 'white')
        elif action.name == 'ALLIN':
            return colors.color(
                '{}{} is all in.'.format(spacing(self.get_betlevel()), p), 'gray')
        else:
            raise Exception('Error processing the action!')

    def invested(self, player):
        return self.stacks[player.name] - player.chips

    def cost(self, amt_invested):
        return (self.betsize * self.get_betlevel()) - amt_invested

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
            self.bettor = poker.bringin(self.r._table)
            self.closer = self.r._table.next_player(self.bettor, -1, hascards=True)
        else:
            # Go with high-hand
            # Default to lowest seat #, change this later.
            self.bettor = poker.highhand(self.r._table, self.r.gametype)[0]
            self.closer = self.r._table.next_player(self.bettor, -1, hascards=True)

    def set_betsize(self):
        if self.r.street > len(self.r.streets):
            raise Exception('The street is larger than the number of streets in the game!')
        else:
            self.betsize = self.r.streets[self.r.street] * self.r.blinds.BB

    def get_bet(self):
        bet = 0
        for p in self.r._table:
            i = self.invested(p)
            if i > bet:
                bet = i
        return bet

    def get_betlevel(self):
        return self.bet // self.betsize

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
            self.stacks = self.r.starting_stacks
        elif self.r.street > 0:
            self.stacks = self.r._table.stackdict()


def calc_odds(bet, pot):
    """
    Calculate the odds offered to a player given a bet amount and a pot amount.
    """
    if bet < 0 or pot < 0:
        raise ValueError('bet or pot must be positive!')
    odds = pot / bet
    return odds


def menu(options=None):
    """
    Display a list of betting options for the current player.
    """
    nice_opts = ['[' + colors.color(v.name[0], 'white', STYLE='BOLD') + ']' +
                 v.name[1:].lower()
                 for k, v in sorted(options.items())]
    choices = '/'.join(nice_opts)

    print('')
    while True:
        choice = input('{}? :> '.format(choices))

        if choice == 'q':
            exit()
        elif choice.lower() in options:
            return options[choice]
        else:
            print('Invalid choice, try again.')


def spacing(level):
    """
    Spaces the player actions by the current bet level.
    """
    return '  ' * level


def one_left(table):
    cardholders = table.get_players(hascards=True)
    if len(cardholders) == 1:
        return cardholders.pop()
    else:
        return None
