import hand
import names
import random
import player_5draw
import player_5stud

TYPES = ['FISH', 'JACKAL', 'MOUSE', 'LION']
BANKDEFAULT = 10000


class Player():
    def __init__(self, name, playertype="None"):
        self.set_name(name)
        self.chips = 0
        self._hand = hand.Hand()

        if playertype is None:
            # Choose random player type
            rnd_type = random_type()
            self.playertype = rnd_type
        else:
            self.playertype = playertype

    def __str__(self):
        """
        Returns the player's name.
        """
        return '{}'.format(self.name)

    def __repr__(self):
        """
        Same as str, returns name.
        """
        return str(self)

    def set_name(self, name):
        """
        Checks the player name, and sets it if valid. Raises an exception if not valid.
        """
        if names.is_validname(name):
            self.name = name
        else:
            raise ValueError('Invalid username "{}" for object!'.format(name))

    def withdraw(self, amt):
        """
        Removes the amount given from the player's stack and returns it. If the amount is more
        than the player has, then the remaining amount in the player's stack is remoevd and
        returned.
        """
        if amt < 0:
            raise ValueError('Player cannot bet a negative amount!')
        if amt > self.chips:
            # Put the player all-in
            amt = self.chips
            self.chips = 0
            return amt
        else:
            self.chips -= amt
            return amt

    def deposit(self, amt):
        """
        Adds the specified amount of chips to the player's stack.
        """
        if amt < 0:
            raise Exception('Cannot add negative chips!')
        else:
            self.chips += amt

    def is_human(self):
        """
        Returns True if the player is a HUMAN type, False otherwise.
        """
        return self.playertype == 'HUMAN'


def random_type():
    return random.choice(TYPES)


class Player5Card(Player):
    def __init__(self, name, playertype=None):
        super().__init__(name, playertype)
        self.chips = BANKDEFAULT
        self.strategies = {}
        self.strategies = player_5draw.TYPES[self.playertype]


class Player5Stud(Player):
    def __init__(self, name, playertype=None):
        super().__init__(name, playertype)
        self.chips = BANKDEFAULT
        self.strategies = {}
        self.strategies = player_5stud.TYPES[self.playertype]
