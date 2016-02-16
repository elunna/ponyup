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

HI_AQ = 1412000000
PAIR_22 = evaluator.HANDTYPES['PAIR']
PAIR_66 = 20600000000
PAIR_JJ = 21100000000
PAIR_AA = 21400000000
TWOPAIR_22 = 30000000000
TWOPAIR_JJ = 31100000000
TRIPS = 40000000000


class Strategy():
    def __init__(self, preflop, postflop):
        self.preflop_play = preflop[0]
        self.preflop_raise = preflop[1]

        self.postflop_play = postflop[0]
        self.postflop_raise = postflop[1]

    def makeplay(self, options, handvalue, street):
        if street == 0:
            return self.play_preflop(options, handvalue)
        elif street == 1:
            return self.play_postflop(options, handvalue)

    def play_preflop(self, options, handvalue):
        if handvalue >= self.preflop_raise:
            if 'r' in options:
                return options['r']
            elif 'c' in options:
                return options['c']
        elif handvalue >= self.preflop_play:
            # All options will be 'c' options here.
            return options['c']
        else:
            if 'f' in options:
                return options['f']
            elif 'c' in options:
                return options['c']
            else:
                raise ValueError('Appropriate key - FOLD/CHECK not in options!')

    def play_postflop(self, options, handvalue):
        if handvalue >= self.postflop_raise:
            if 'r' in options:
                return options['r']
            elif 'b' in options:
                return options['b']
            elif 'c' in options:
                return options['c']
        elif handvalue >= self.postflop_play:
            if 'b' in options:
                return options['b']
            else:
                return options['c']
        else:
            if 'f' in options:
                return options['f']
            elif 'c' in options:
                return options['c']
            else:
                raise ValueError('Appropriate key - FOLD/CHECK not in options!')


def get_superfish():
    pre = [0, PAIR_AA]
    post = [PAIR_AA, TWOPAIR_JJ]
    return Strategy(pre, post)


def get_aggrofish():
    pre = [0, HI_AQ]
    post = [PAIR_AA, TWOPAIR_22]
    return Strategy(pre, post)


def get_normal():
    pre = [PAIR_66, PAIR_JJ]
    post = [PAIR_AA, TWOPAIR_JJ]
    return Strategy(pre, post)


def get_tight():
    pre = [PAIR_66, PAIR_AA]
    post = [TWOPAIR_22, TRIPS]
    return Strategy(pre, post)
