import hand
import player
import pokerhands
import random


FISH = {
    'pre_call': 0,
    'pre_raise': pokerhands.PAIR_AA,
    'post_call': pokerhands.PAIR_AA,
    'post_raise': pokerhands.TWOPAIR_JJ,
    'bluff': 5,
}


JACKAL = {
    'pre_call': 0,
    'pre_raise': pokerhands.HI_AQ,
    'post_call': pokerhands.PAIR_22,
    'post_raise': pokerhands.PAIR_66,
    'bluff': 25,
}


MOUSE = {
    'pre_call': pokerhands.PAIR_66,
    'pre_raise': pokerhands.PAIR_AA,
    'post_call': pokerhands.PAIR_AA,
    'post_raise': pokerhands.TRIPS,
    'bluff': 5,
}


LION = {
    'pre_call': pokerhands.PAIR_66,
    'pre_raise': pokerhands.PAIR_66,
    'post_call': pokerhands.PAIR_66,
    'post_raise': pokerhands.TWOPAIR_JJ,
    'bluff': 10,
}


TYPES = {
    'FISH': FISH,
    'JACKAL': JACKAL,
    'MOUSE': MOUSE,
    'LION': LION,
}


class Player5Card(player.Player):
    def __init__(self, name, playertype=None):
        self.set_name(name)
        self._type = playertype

        if playertype is None:
            self.strat = random.choice(list(TYPES.keys()))
        elif playertype not in TYPES:
            raise ValueError('type argument is not valid.')
        else:
            self.strat = TYPES[playertype]

        self.chips = 0
        self._hand = hand.Hand()
