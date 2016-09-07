from collections import namedtuple

Level = namedtuple('Level', ['BB', 'SB', 'ANTE', 'BRINGIN'])


class Blinds():
    def __init__(self, level=1, structure_dict=None):
        """
        Initialize the Blinds object with a given blind structure, or use the default house
        structure.
        """
        if structure_dict is None:
            raise ValueError("Need a blind structure!")
        else:
            self.blind_dict = structure_dict

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
        return show_stakes(self.blind_dict[self.level])

    def set_level(self, level):
        """
        Set the blind level, if valid.
        """
        if level < 1 or level > len(self.blind_dict):
            raise ValueError('level is out of bounds!')

        self.level = level

        self.BB = self.blind_dict[level].BB
        self.SB = self.blind_dict[level].SB
        self.ANTE = self.blind_dict[level].ANTE
        self.BRINGIN = self.blind_dict[level].BRINGIN

    def levels(self):
        """
        Returns a listing of all the available blind levels in the structure.
        """
        for k, v in sorted(self.blind_dict.items()):
            print('\tLevel {:3}: ${}/${}'.format(k, v.BB, v.BB * 2))


def show_stakes(lev):
    """
    Returns the stakes, as in the small bet/big bet amounts. For games that only use blinds
    (without antes), we calculate the amounts by using the Big Blind as the small bet, and
    twice the Big Blind as the big bet.
    """
    return '${}/${}'.format(lev.BB, lev.BB * 2)


def noante_level(sb, bb):
    return Level(sb, bb, 0, 0)


class BlindsAnte(Blinds):
    def __init__(self, level=1):
        super().__init__(level, structure_dict=ante)

    def sb_to_ante_ratio(self):
        """
        Returns the SB-to-Ante ratio of the current small blind and ante.
        """
        # Use only one decimal place.
        if self.ANTE > 0:
            return round(self.SB / self.ANTE, 1)
        else:
            return 0


class BlindsNoAnte(Blinds):
    def __init__(self, level=1):
        super().__init__(level, structure_dict=no_ante)


no_ante = {
    1:  noante_level(1, 0.50),
    2:  noante_level(2, 1),
    3:  noante_level(3, 1),
    4:  noante_level(4, 2),
    5:  noante_level(6, 3),
    6:  noante_level(8, 4),
    7:  noante_level(15, 10),
    8:  noante_level(20, 10),
    9:  noante_level(30, 15),
    10: noante_level(50, 25),
}

# Since there is no Big Blind in these games, the BB represents the "Big Bet", and the SB
# represents the "Small Bet".
ante = {
    1:  Level(BB=1, SB=1, BRINGIN=0.50, ANTE=0.25),
    2:  Level(BB=2, SB=2, BRINGIN=1, ANTE=.50),
    3:  Level(BB=3, SB=3, BRINGIN=1.50, ANTE=0.75),
    4:  Level(BB=4, SB=4, BRINGIN=2, ANTE=1),
    5:  Level(BB=6, SB=6, BRINGIN=3, ANTE=1.5),
    6:  Level(BB=8, SB=8, BRINGIN=4, ANTE=1.5),
    7:  Level(BB=15, SB=15, BRINGIN=5, ANTE=3),
    8:  Level(BB=20, SB=20, BRINGIN=8, ANTE=4),
    9:  Level(BB=30, SB=25, BRINGIN=10, ANTE=5),
    10: Level(BB=50, SB=50, BRINGIN=20, ANTE=10),
}
