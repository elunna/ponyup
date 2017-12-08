"""
A Token is a button or other object on the table that represents a position, a game state, layer state, or some other piece of info
"""


class Token(object):
    def __init__(self, name, table):
        self.table = table
        self.name = name
        self.seat = None
