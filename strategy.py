import evaluator

"""
    Things a player generally takes into consideration when planning a play:
        * Cards
        * Position
        * Size of pot
        * Pot odds
        * Implied odds
        * Potential negative implied odds
        * Number of players
        * Types of opponents
        * Action beforehand
        * Potential action ahead
        * Stacksizes
        * Game/street situation
        * Meta-game reasons - influence image, bluffing, etc.

    To greatly simplify, we'll just start with cards and handvalue.

"""

PAIR = evaluator.HANDTYPES['PAIR']
PAIR_66 = 20600000000
PAIR_JJ = 21100000000
PAIR_AA = 21400000000
HI_AQ = 1412000000


class Strategy():
    def __init__(self, preflop):
        self.pf_play = preflop[0]
        self.pf_raise = preflop[1]

    def makeplay(self, options, handvalue):
        if handvalue >= self.pf_raise:
            if 'r' in options:
                return options['r']
            elif 'c' in options:
                return options['c']
        elif handvalue >= self.pf_play:
            # All options will be 'c' options here.
            return options['c']
            """
            if 'CALL' in options:
                return options['c']
            if 'COMPLETE' in options:
                returnoptions['c']
            if 'CHECK' in options:
                returnoptions['c']
            """
        else:
            if 'f' in options:
                return options['f']
            elif 'c' in options:
                return options['c']
            else:
                raise ValueError('Appropriate key - FOLD/CHECK not in options!')


def get_superfish():
    return Strategy([0, PAIR_AA])


def get_aggrofish():
    return Strategy([0, HI_AQ])


def get_normal():
    return Strategy([PAIR_66, PAIR_JJ])


def get_tight():
    return Strategy([PAIR_66, PAIR_AA])
