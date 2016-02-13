import evaluator

PAIR = evaluator.HANDTYPES['PAIR']

PAIR_66 = 20600000000
PAIR_JJ = 21100000000
PAIR_AA = 21400000000
HI_AQ = 1412000000


class Strategy():
    def __init__(self, preflop):
        self.pf_play = preflop[0]
        self.pf_raise = preflop[1]


def get_superfish():
    return Strategy([0, PAIR_AA])


def get_aggrofish():
    return Strategy([0, HI_AQ])


def get_normal():
    return Strategy([PAIR_66, PAIR_JJ])


def get_tight():
    return Strategy([PAIR_66, PAIR_AA])
