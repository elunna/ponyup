from __future__ import print_function
from collections import namedtuple
import colors
import strategy
import poker

Action = namedtuple('Action', ['name', 'cost', 'level'])


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

        self.set_level()
        self.set_betsize()
        self.set_stacks()

    def play(self):
        """
        Performs a round of betting between all the players that have cards and chips.
        """
        while True:
            yield self.get_bettor()

            winner = one_left(self.r._table)
            if winner:
                oneleft = '{}Only one player left!'.format(spacing(self.level))
                print(colors.color(oneleft, 'LIGHTBLUE'))
                #  self.playing = False
                raise StopIteration()

            elif self.done():
                # Reached the last bettor, betting is closed.
                raise StopIteration()

            else:
                self.next_bettor()

    def player_decision(self, p):
        invested = self.invested(p)
        cost = (self.betsize * self.level) - invested
        options = self.get_options(cost, p.chips)

        if 'a' in options:
            # Player is allin
            return Action('ALLIN', 0, 0)
        elif p.is_human():
            return menu(options)
        else:
            facing = cost / self.betsize
            return strategy.makeplay(p, options, self.r.street, self.level, facing)

    def process_option(self, action):
        """
        Performs the option picked by a player.
        """
        p = self.get_bettor()

        if action.name == 'FOLD':
            self.r.muck.extend(p.fold())
        elif action.name in ['CHECK', 'ALLIN']:
            return
        elif action.level > 0:
            # It's a bet or raise, so we'll need to reset last better.
            self.closer = self.r._table.next_player(self.bettor, -1, hascards=True)

        self.r.pot += p.bet(action.cost)
        self.level += action.level

    def get_options(self, cost, stack):
        """
        Shows the options available to the current bettor.
        """
        option_dict = {}
        #  completing = (self.betsize - cost) == self.r.blinds.SB

        if stack == 0:
            option_dict['a'] = Action('ALLIN', 0, 0)
            # Save some time
            return option_dict

        if cost == 0:
            option_dict['c'] = Action('CHECK', 0, 0)
        elif cost > 0:
            option_dict['f'] = Action('FOLD', 0, 0)

            if stack >= cost:
                option_dict['c'] = Action('CALL', cost, 0)
            else:
                # Player doesn't have enough for the full call amount
                option_dict['c'] = Action('CALL', stack, 0)

        if self.level == 0:
            # Player doesn't have enough for the full bet amount
            if stack >= self.betsize:
                option_dict['b'] = Action('BET', self.betsize, 1)
            else:
                option_dict['b'] = Action('BET', stack, 1)

        if self.level >= 1 and self.level < self.BETCAP:
            raise_cost = cost + self.betsize

            if stack < self.betsize:
                # Player does not have enough chips for a raise.
                pass
            elif stack >= raise_cost:
                option_dict['r'] = Action('RAISE', raise_cost, 1)
            else:
                # Player doesn't have enough for a full raise, but enough for a partial raise.
                option_dict['r'] = Action('RAISE', stack, 1)

        return option_dict

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

    def set_level(self):
        if self.r.street == 0:
            self.level = 1
        else:
            self.level = 0

    def set_betsize(self):
        if self.r.street > len(self.r.streets):
            raise Exception('The street is larger than the number of streets in the game!')
        else:
            self.betsize = self.r.streets[self.r.street] * self.r.blinds.BB

    def set_stacks(self):
        if self.r.street == 0:
            self.stacks = self.r.starting_stacks
        elif self.r.street > 0:
            self.stacks = self.r._table.stackdict()

    def get_bettor(self):
        """
        Returns the current active bettor.
        """
        return self.r._table.seats[self.bettor]

    def get_closer(self):
        """
        Returns the player who will close the betting.
        """
        return self.r._table.seats[self.closer]

    def invested(self, player):
        return self.stacks[player.name] - player.chips

    def cost(self, amt_invested):
        return (self.betsize * self.level) - amt_invested

    def next_bettor(self):
        self.bettor = self.r._table.next_player(self.bettor, hascards=True)

    def done(self):
        return self.bettor == self.closer

    def action_string(self, action):
        p = self.get_bettor()
        act_str = ''
        act_str += spacing(self.level)
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
            return colors.color('{}{} is all in.'.format(spacing(self.level), p), 'gray')
        else:
            raise Exception('Error processing the action!')


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
