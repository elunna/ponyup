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
