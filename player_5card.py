import hand
import player
import evaluator

HI_AQ = 1412000000
PAIR_22 = evaluator.HANDTYPES['PAIR']
PAIR_66 = 20600000000
PAIR_JJ = 21100000000
PAIR_AA = 21400000000
TWOPAIR_22 = 30000000000
TWOPAIR_JJ = 31100000000
TRIPS = 40000000000

FISH = {
    'pre_call': 0,
    'pre_raise': PAIR_AA,
    'post_call': PAIR_AA,
    'post_raise': TWOPAIR_JJ,
    'bluff': 5,
}


JACKAL = {
    'pre_call': 0,
    'pre_raise': HI_AQ,
    'post_call': PAIR_22,
    'post_raise': PAIR_66,
    'bluff': 25,
}


MOUSE = {
    'pre_call': PAIR_66,
    'pre_raise': PAIR_AA,
    'post_call': PAIR_AA,
    'post_raise': TRIPS,
    'bluff': 5,
}


LION = {
    'pre_call': PAIR_66,
    'pre_raise': PAIR_66,
    'post_call': PAIR_66,
    'post_raise': TWOPAIR_JJ,
    'bluff': 10,
}


TYPES = {
    'FISH': FISH,
    'JACKAL': JACKAL,
    'MOUSE': MOUSE,
    'LION': LION,
}


class Player5Card(player.Player):
    def __init__(self, name, playertype='FISH'):
        self.set_name(name)
        self.playertype = playertype

        if playertype not in TYPES:
            raise ValueError('type argument is not valid.')
        else:
            self.strat = TYPES[playertype]

        self.chips = 0
        self._hand = hand.Hand()
