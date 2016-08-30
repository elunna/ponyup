from __future__ import print_function
from collections import namedtuple
import colors
import strategy

Action = namedtuple('Action', ['name', 'cost', 'level'])


class BettingRound():
    def __init__(self, r):
        """
        Manages the betting info and activities. Takes in a Round object as r.
        """
        self.r = r
        self.BETCAP = 4
        self.set_bettor_and_closer()

        # Preflop: Headsup
        if r.street == 0:
            # Preflop the first bettor is right after the BB
            self.level = 1
            self.betsize = r.blinds.BB

            # Copy the starting stack for the first round (because blinds were posted)
            self.betstack = r.starting_stacks

        elif r.street > 0:
            # postflop the first bettor is right after the button
            self.level = 0
            self.betsize = r.blinds.BB * 2
            self.betstack = r._table.stackdict()

    def play(self):
        """
        Performs a round of betting between all the players that have cards and chips.
        """
        playing = True

        while playing:
            p = self.get_bettor()
            invested = self.betstack[p.name] - p.chips
            cost = (self.betsize * self.level) - invested
            options = self.get_options(cost)

            if p.is_allin():
                o = allin_option()
            elif p.is_human():
                print('pot is {}'.format(self.r.pot))
                o = menu(options)
            else:
                o = strategy.makeplay(p, self.r, options)

            action_string = self.process_option(o)
            print(action_string)

            cardholders = self.r._table.get_players(CARDS=True)

            if len(cardholders) == 1:
                oneleft = '{}Only one player left!'.format(spacing(self.level))
                print(colors.color(oneleft, 'LIGHTBLUE'))
                return cardholders.pop()

            elif self.bettor == self.closer:
                # Reached the last bettor, betting is closed.
                playing = False
            else:
                # Set next bettor
                self.bettor = self.r._table.next_player_w_cards(self.bettor)

        else:
            # The betting round is over, and there are multiple players still remaining.
            return None

    def process_option(self, action):
        """
        Performs the option picked by a player.
        """
        p = self.get_bettor()
        actualbet = 0

        if action.name == 'FOLD':
            self.r.muck.extend(p.fold())
        elif action.name == 'ALLIN':
            return colors.color('{}{} is all in.'.format(spacing(self.level), p), 'gray')
        elif action.level > 0:
            # It's a raise, so we'll need to reset last better.
            self.closer = self.r._table.next_player_w_cards(self.bettor, -1)
            actualbet = p.bet(action.cost)
            self.r.pot += actualbet
            self.level += action.level
        else:
            actualbet = p.bet(action.cost)
            self.r.pot += actualbet

        act_str = ''
        act_str += spacing(self.level)
        act_str += '{} {}s'.format(p, action.name.lower())

        amt = colors.color(' $' + str(actualbet), 'yellow')

        if action.name in ['BET', 'RAISE']:
            return colors.color(act_str, 'red') + amt
        elif action.name == 'FOLD':
            return colors.color(act_str, 'purple')
        elif action.name == 'CHECK':
            return colors.color(act_str, 'white')
        else:
            return colors.color(act_str, 'white') + amt

    def get_options(self, cost):
        """
        Shows the options available to the current bettor.
        """
        completing = (self.betsize - cost) == self.r.blinds.SB

        option_dict = {}

        if self.r.street == 0 and completing:
            # Completing the small blind
            option_dict['f'] = Action('FOLD', 0, 0)
            option_dict['c'] = Action('COMPLETE', cost, 0)
            option_dict['r'] = Action('RAISE', cost + self.betsize, 1)

        elif cost == 0 and self.level >= 1:
            # Typical BB, Straddle, or post situation.
            option_dict['c'] = Action('CHECK', 0, 0)
            option_dict['r'] = Action('RAISE', cost + self.betsize, 1)

        elif cost == 0 and self.level == 0:
            # Noone has opened betting yet on a postblind round
            option_dict['c'] = Action('CHECK', 0, 0)
            option_dict['b'] = Action('BET', self.betsize, 1)

        elif cost > 0 and self.level < self.BETCAP:
            # There has been a bet/raises, but still can re-raise
            option_dict['f'] = Action('FOLD', 0, 0)
            option_dict['c'] = Action('CALL', cost, 0)
            option_dict['r'] = Action('RAISE', cost + self.betsize, 1)

        elif cost > 0 and self.level == self.BETCAP:
            # The raise cap has been met, can only call or fold.
            option_dict['f'] = Action('FOLD', 0, 0)
            option_dict['c'] = Action('CALL', cost, 0)

        return option_dict

    def set_bettor_and_closer(self):
        if self.r.street == 0:
            self.closer = self.r._table.TOKENS['BB']
            self.bettor = self.r._table.next(self.closer)
        else:
            self.bettor = self.r._table.next_player_w_cards(self.r._table.TOKENS['D'])
            self.closer = self.r._table.next_player_w_cards(self.bettor, -1)

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


def allin_option():
    """
    Returns the option for players that are all-in.
    """
    return Action('ALLIN', 0, 0)


def spacing(level):
    """
    Spaces the player actions by the current bet level.
    """
    return '  ' * level
