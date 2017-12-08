import random

""" The Button module manages the movement of the Dealer Button.
"""


def move_button(table):
    """ Moves the button to the next valid player/seat and sets the blinds. """
    table.TOKENS['D'] = table.next_player(table.TOKENS['D'])


def randomize_button(table):
    """ Places the button at a random player's seat. If there is no players
        at the table, it raises an Exception.
    """
    seats = list(table.get_playerdict().keys())
    if len(seats) == 0:
        raise Exception('Cannot place the button, no players at table!')
    choice = random.choice(seats)
    table.TOKENS['D'] = choice
