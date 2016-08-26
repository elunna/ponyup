import blinds_house


class Blinds():
    def __init__(self, level=1):
        self.blind_dict = blinds_house.house_limits
        self.set_level(level)

    def set_level(self, level):
        if level < 1 or level > len(self.blind_dict):
            raise ValueError('level is out of bounds!')
        self.BB = self.blind_dict.get(str(level))[0]
        self.SB = self.blind_dict.get(str(level))[1]
        self.ANTE = self.blind_dict.get(str(level))[2]

    def sb_to_ante_ratio(self):
        # Use only one decimal place.
        if self.ANTE > 0:
            return round(self.SB / self.ANTE, 1)
        else:
            return 0

    def stakes(self):
        if self.ANTE > 0:
            return '${}/${}, Ante: ${}'.format(self.BB, self.BB * 2, self.ANTE)
        else:
            return '${}/${}'.format(self.BB, self.BB * 2)

    def levels(self):
        for i in range(1, len(self.blind_dict) + 1):
            print('Level {}: ${}/${}, Ante ${}'.format(i,
                                                       self.blind_dict.get(i)[0],
                                                       self.blind_dict.get(i)[1],
                                                       self.blind_dict.get(i)[2]))
