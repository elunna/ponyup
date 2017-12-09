"""
  " Tools for using the Joker in a playing card games.
  """
from . import playingcard as pc

joker_rank, joker_suit = 'Z', 's'


class Joker(pc.PlayingCard):
    """ Manages a single instance of a Card """
    def __init__(self):
        pc.PlayingCard.__init__(self, joker_rank, joker_suit)
