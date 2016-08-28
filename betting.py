from __future__ import print_function


def calc_odds(bet, pot):
    """ Calculate the odds offered to a player given a bet amount and a pot amount."""
    if bet < 0 or pot < 0:
        raise ValueError('bet or pot must be positive!')
    odds = pot / bet
    return odds


def menu(options=None):
    """
    Display a list of betting options for the current player.
    """
    # Sort by chip cost
    optlist = [(options[o][1], o, options[o][0][1:]) for o in options]

    for o in sorted(optlist):
        print('({}){}--${} '.format(o[1], o[2], o[0]), end='')

    print('')
    while True:
        choice = input(':> ')

        if choice == 'q':
            exit()
        elif choice.lower() in options:
            return options[choice]
        else:
            print('Invalid choice, try again.')


def get_options(cost, env):
    """ Shows the options available to the current bettor."""
    completing = (env.betsize - cost) == env._session.blinds.SB

    OPTIONS = {}

    if env.street == 0 and completing:
        # Completing the small blind
        OPTIONS['f'] = ('FOLD', 0, 0)
        OPTIONS['c'] = ('COMPLETE', cost, 0)
        OPTIONS['r'] = ('RAISE', cost + env.betsize, 1)

    elif cost == 0 and env.level >= 1:
        # Typical BB, Straddle, or post situation.
        OPTIONS['c'] = ('CHECK', 0, 0)
        OPTIONS['r'] = ('RAISE', cost + env.betsize, 1)

    elif cost == 0 and env.level == 0:
        # Noone has opened betting yet on a postblind round
        OPTIONS['c'] = ('CHECK', 0, 0)
        OPTIONS['b'] = ('BET', env.betsize, 1)

    elif cost > 0 and env.level < env.betcap:
        # There has been a bet/raises, but still can re-raise
        OPTIONS['f'] = ('FOLD', 0, 0)
        OPTIONS['c'] = ('CALL', cost, 0)
        OPTIONS['r'] = ('RAISE', cost + env.betsize, 1)

    elif cost > 0 and env.level == env.betcap:
        # The raise cap has been met, can only call or fold.
        OPTIONS['f'] = ('FOLD', 0, 0)
        OPTIONS['c'] = ('CALL', cost, 0)

    return OPTIONS
