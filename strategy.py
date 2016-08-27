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


class Strategy():
    def __init__(self):
        self.pre_call = None
        self.pre_raise = None
        self.post_call = None
        self.post_raise = None
        self.bluff = None


def makeplay(player, _game, options):
    handval = player._hand.value

    if _game.street == 0:

        if handval >= player.strat['pre_raise']:
            return pick_raise(options)
        elif handval >= player.strat['pre_call']:
            return pick_call(options)
        else:
            return pick_other(options)

    elif _game.street == 1:
        if handval >= player.strat['post_raise']:
            return pick_raise(options)
        elif handval >= player.strat['post_call']:
            return pick_call(options)
        else:
            return pick_other(options)


def pick_raise(options):
    if 'r' in options:
        return options['r']
    elif 'b' in options:
        return options['b']
    elif 'c' in options:
        return options['c']


def pick_call(options):
    if 'b' in options:
        return options['b']
    else:
        return options['c']


def pick_other(options):
    if 'f' in options:
        return options['f']
    elif 'c' in options:
        return options['c']
    else:
        raise ValueError('Appropriate key - FOLD/CHECK not in options!')
