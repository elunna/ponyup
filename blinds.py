from collections import namedtuple
import math

Level = namedtuple('Level', ['BB', 'SB', 'ANTE', 'BRINGIN'])


class Blinds():
    def __init__(self, level=1, structure=None):
        """
        Initialize the Blinds object with a given blind structure.
        """
        if structure is None:
            raise ValueError("Need a blind structure!")
        else:
            self.structure = structure

        self.set_level(level)

    def __str__(self):
        """
        Returns the stakes, as in the small bet/big bet amounts.
        Note: For ante/bringin games, the small-bet is SB and the big-bet is BB.
        """
        _str = ''
        if self.ANTE:
            _str += 'Ante: ${:.2f}\n'.format(self.ANTE)
        if self.BRINGIN:
            _str += 'Bringin: ${:.2f}\n'.format(self.BRINGIN)
        if self.SB != self.BB:
            _str += 'SB: ${}, BB: ${}\n'.format(self.SB, self.BB)

        return _str

    def stakes(self):
        """
        Returns the stakes, as in the small bet/big bet amounts. For games that only use blinds
        (without antes), we calculate the amounts by using the Big Blind as the small bet, and
        twice the Big Blind as the big bet.
        """
        return '${}/${}'.format(self.BB, self.BB * 2)

    def set_level(self, level):
        """
        Set the blind level, if valid.
        """
        if level < 1 or level > len(self.structure):
            raise ValueError('level is out of bounds!')

        self.level = level
        leveltuple = tuple_to_level(self.structure[level])
        self.BB = leveltuple.BB
        self.SB = leveltuple.SB
        self.ANTE = leveltuple.ANTE
        self.BRINGIN = leveltuple.BRINGIN

    def levels(self):
        """
        Returns a listing of all the available blind levels in the structure.
        """
        for k, v in sorted(self.structure.items()):
            print('\tLevel {:3}: ${}/${}'.format(k, v.BB, v.BB * 2))

    def big_blinds(self, stack):
        """
        Returns how many big blinds are in the stack. Uses the Big Blind from the current level
        and rounds down.
        """
        return round_number(stack / self.BB)

    def eff_big_blinds(self, stack, players):
        """
        Returns how many big blinds are effectively in the stack. First adds up the current pot
        which is (SB + BB + Antes). The players variable is an integer which specified how many
        antes to add. Then the effective big blind is 2/3rds of the pot. Returns a rounded
        integer.
        """
        pot = self.SB + self.BB + (players * self.ANTE)
        return round_number(pot * .66)

    def sb_to_ante_ratio(self):
        """
        Returns the SB-to-Ante ratio of the current small blind and ante.
        """
        # Use only one decimal place.
        if self.ANTE > 0:
            return round(self.SB / self.ANTE, 1)
        else:
            return 0


class BlindsAnte(Blinds):
    def __init__(self, level=1):
        super().__init__(level, structure=ante)


class BlindsNoAnte(Blinds):
    def __init__(self, level=1):
        super().__init__(level, structure=no_ante)


def tuple_to_level(lev):
    if len(lev) == 2:
        # There is only SB and BB
        return Level(BB=lev[0], SB=lev[1], BRINGIN=0, ANTE=0)
    elif len(lev) == 3:
        # There is SB, BB, and antes
        return Level(BB=lev[0], SB=lev[1], BRINGIN=0, ANTE=lev[2])
    elif len(lev) == 4:
        # There is SB, BB, bringin, and antes
        return Level(BB=lev[0], SB=lev[1], BRINGIN=lev[2], ANTE=lev[3])


def round_number(num):
    if num % 1 >= 0.5:
        return math.ceil(num)
    else:
        return math.floor(num)


no_ante = {
    1:  (1, 0.50),
    2:  (2, 1),
    3:  (3, 1),
    4:  (4, 2),
    5:  (6, 3),
    6:  (8, 4),
    7:  (15, 10),
    8:  (20, 10),
    9:  (30, 15),
    10: (50, 25),
}

# Since there is no Big Blind in these games, the BB represents the "Big Bet", and the SB
# represents the "Small Bet".
ante = {
    # BB, SB, BRINGIN, ANTE
    1:  (1, 1, 0.50, 0.25),
    2:  (2, 2, 1, .50),
    3:  (3, 3, 1.50, 0.75),
    4:  (4, 4, 2, 1),
    5:  (6, 6, 3, 1.5),
    6:  (8, 8, 4, 1.5),
    7:  (15, 15, 5, 3),
    8:  (20, 20, 8, 4),
    9:  (25, 25, 10, 5),
    10: (50, 50, 20, 10),
}
