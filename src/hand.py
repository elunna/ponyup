""" Manages a regular hand of cards. """

from . import evaluator
from . import cardlist


class Hand(evaluator.PokerHand, cardlist.CardList):
    """ Poker Hand object """
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
