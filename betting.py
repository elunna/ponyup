from __future__ import print_function
from collections import namedtuple
import colors

Option = namedtuple('Option', ['action', 'cost', 'level'])


def calc_odds(bet, pot):
    """ Calculate the odds offered to a player given a bet amount and a pot amount."""
    if bet < 0 or pot < 0:
        raise ValueError('bet or pot must be positive!')
    odds = pot / bet
    return odds


def menu(options=None):
    """ Display a list of betting options for the current player. """
    nice_opts = ['[' + colors.color(v.action[0], 'white', STYLE='BOLD') + ']' +
                 v.action[1:].lower()
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
    return Option('ALLIN', 0, 0)


def get_options(cost, env):
    """ Shows the options available to the current bettor."""
    completing = (env.betsize - cost) == env._session.blinds.SB

    option_dict = {}

    if env.street == 0 and completing:
        # Completing the small blind
        option_dict['f'] = Option('FOLD', 0, 0)
        option_dict['c'] = Option('COMPLETE', cost, 0)
        option_dict['r'] = Option('RAISE', cost + env.betsize, 1)

    elif cost == 0 and env.level >= 1:
        # Typical BB, Straddle, or post situation.
        option_dict['c'] = Option('CHECK', 0, 0)
        option_dict['r'] = Option('RAISE', cost + env.betsize, 1)

    elif cost == 0 and env.level == 0:
        # Noone has opened betting yet on a postblind round
        option_dict['c'] = Option('CHECK', 0, 0)
        option_dict['b'] = Option('BET', env.betsize, 1)

    elif cost > 0 and env.level < env.betcap:
        # There has been a bet/raises, but still can re-raise
        option_dict['f'] = Option('FOLD', 0, 0)
        option_dict['c'] = Option('CALL', cost, 0)
        option_dict['r'] = Option('RAISE', cost + env.betsize, 1)

    elif cost > 0 and env.level == env.betcap:
        # The raise cap has been met, can only call or fold.
        option_dict['f'] = Option('FOLD', 0, 0)
        option_dict['c'] = Option('CALL', cost, 0)

    return option_dict


def process_option(option, env):
    """ Performs the option picked by a player. """
    p = env._table.seats[env.bettor]

    if option[0] == 'FOLD':
        env.muck.extend(p.fold())
    elif option[0] == 'ALLIN':
        return '{} is all in.'.format(p)
    elif option[2] > 0:
        # It's a raise, so we'll need to reset last better.
        env.closer = env._table.next_player_w_cards(env.bettor, -1)
        env.pot += p.bet(option[1])
        env.level += option[2]
    else:
        env.pot += p.bet(option[1])

    act_str = ''
    act_str += '  ' * env.level
    act_str += '{} {}s'.format(p, option[0].lower())

    amt = colors.color(' $' + str(option[1]), 'yellow')

    if option[0] in ['BET', 'RAISE']:
        return colors.color(act_str, 'red') + amt
    elif option[0] in ['FOLD', 'CHECK']:
        return colors.color(act_str, 'purple')
    else:
        return colors.color(act_str, 'white') + amt
