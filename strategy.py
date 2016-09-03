"""
Considerations when planning a play:
    * Cards
    * Position
    * Stacksizes
    * Size of pot, Pot odds, and Implied odds. Also negative implied odds.
    * Number and type of opponents
    * Action beforehand and potential action ahead
    * Game/street situation
    * Meta-game reasons - influence image, bluffing, etc.
To greatly simplify, we'll just start with cards and handvalue.
"""


def makeplay(player, options, street, betlevel, facing):
    """
    Determines the appropriate play based on the street and handstrength.
    """
    handval = player._hand.value()
    strat = player.strategies[street + 1]

    if betlevel == 0:
        if handval >= strat.bet:
            return pick_raise(options)
        elif handval >= strat.call1:
            return pick_call(options)
        else:
            return pick_fold_or_check(options)

    elif betlevel == 1:
        if handval >= strat.raise1:
            return pick_raise(options)
        elif handval >= strat.call1:
            return pick_raise(options)
        else:
            return pick_fold_or_check(options)

    elif betlevel > 1:
        if handval >= strat.raise2:
            return pick_raise(options)
        elif facing == 2 and handval >= strat.call2:
            return pick_call(options)
        elif facing == 1 and handval >= strat.call1:
            return pick_call(options)
        else:
            return pick_fold_or_check(options)


def pick_raise(options):
    """
    Pick the most aggressive action available
    RAISE > BET > CALL
    """
    if 'r' in options:
        return options['r']
    elif 'b' in options:
        return options['b']
    elif 'c' in options:
        return options['c']


def pick_call(options):
    """
    Pick the 1-bet option
    BET > CALL
    """
    if 'b' in options:
        return options['b']
    else:
        return options['c']


def pick_fold_or_check(options):
    """
    Pick the passive option
    FOLD or check/call
    """
    if 'f' in options:
        return options['f']
    elif 'c' in options:
        return options['c']
    else:
        raise ValueError('Appropriate key - FOLD/CHECK not in options!')
