from __future__ import print_function
from collections import namedtuple


def calc_odds(bet, pot):
    """ Calculate the odds offered to a player given a bet amount and a pot amount."""
    if bet < 0 or pot < 0:
        raise ValueError('bet or pot must be positive!')
    odds = pot / bet
    return odds


def menu(options=None):
    """ Display a list of betting options for the current player. """

    picks = '/'.join([v.action.title() for k, v in sorted(options.items())])

    print('')
    while True:
        choice = input('{}? :> '.format(picks))

        if choice == 'q':
            exit()
        elif choice.lower() in options:
            return options[choice]
        else:
            print('Invalid choice, try again.')


def get_options(cost, env):
    """ Shows the options available to the current bettor."""
    completing = (env.betsize - cost) == env._session.blinds.SB

    option_dict = {}
    Option = namedtuple('Option', ['action', 'cost', 'level'])

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
