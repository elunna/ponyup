"""
  " Tools for analyzing stack sizes at tables or tournaments.
  """
import random

MIN_BB, MAX_BB = 5, 50


def largest(table):
    """ Return the largest stack size of the active players(with cards) at the table. """
    players = table.get_players(hascards=True)
    return max([s.stack for s in players])


def smallest(table):
    """ Return the smallest stack size of the active players(with cards) at the table. """
    players = table.get_players(hascards=True)
    return min([s.stack for s in players])


def average(table):
    """ Return the average stack size of active players(with cards) at the table. """
    players = table.get_players(hascards=True)
    total = sum([s.stack for s in players])
    return total / len(players)


def effective(table):
    """ Return the effective stack size at the table.
        If there are only 2 active players, it is the smaller of the 2 stacks.
        If there are multiple active players, it is the average of all the stacks.
    """
    players = table.get_players(hascards=True)
    if len(players) == 2:
        return smallest(table)
    else:
        return average(table)


def random_stack(bb):
    """ Takes in a big blind size and generates a random stack size between
        MIN_BB and MAX_BB.
    """
    bigblinds = random.randint(MIN_BB, MAX_BB)
    return bigblinds * bb
