"""
Hand history logger. Logs the actions that take place during a round of poker.

For a normal hand history file, we will start with a header:
        * PonyupPoker Poker Game
        * Game ID#
        * Table name,
        * stakes,
        * Game type
        * time,
        * date
        * Seats, names, stack sizes
"""


class HandHistory():
    def __init__(self, _round):
        pass
        self.text = ''

    def write_header(self):
        self.text += 'PonyUp Poker'

    def log(self, text):
        self.text += text
