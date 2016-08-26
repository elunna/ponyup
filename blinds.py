import blinds_house


class Blinds():
    def __init__(self, structure_dict=None, level=1):
        if structure_dict is None:
            self.blind_dict = blinds_house.house_limits
        else:
            self.blind_dict = structure_dict
        self.set_level(level)

    def __str__(self):
        if self.ANTE > 0:
            return '${}/${}, Ante: ${}'.format(self.BB, self.BB * 2, self.ANTE)
        else:
            return '${}/${}'.format(self.BB, self.BB * 2)

    def set_level(self, level):
        if level < 1 or level > len(self.blind_dict):
            raise ValueError('level is out of bounds!')
        self.BB, self.SB, self.ANTE = self.blind_dict.get(level)

    def sb_to_ante_ratio(self):
        # Use only one decimal place.
        if self.ANTE > 0:
            return round(self.SB / self.ANTE, 1)
        else:
            return 0

    def levels(self):
        for k in sorted(self.blind_dict.keys()):
            print('Level {}: ${}/${}, Ante ${}'.format(k, *self.blind_dict[k]))
