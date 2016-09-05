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
        """
        if self.ANTE > 0:
            return '${}/${}, Ante: ${}'.format(self.BB, self.BB * 2, self.ANTE)
        else:
            return '${}/${}'.format(self.BB, self.BB * 2)

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

    def sb_to_ante_ratio(self):
        """
        Returns the SB-to-Ante ratio of the current small blind and ante.
        """
        # Use only one decimal place.
        if self.ANTE > 0:
            return round(self.SB / self.ANTE, 1)
        else:
            return 0

    def levels(self):
        """
        Returns a listing of all the available blind levels in the structure.
        """
        for k in sorted(self.blind_dict.keys()):
            BB, SB, ante = self.blind_dict[k]
            blinds = '${}/${}'.format(BB, BB * 2)
            print('\tLevel {:3}: {:15} Ante ${}'.format(k, blinds, ante))


def noante_level(sb, bb):
    return Level(sb, bb, 0, 0)
