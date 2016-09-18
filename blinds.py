import math


class Blinds():
    def __init__(self, level=1, blinds=True, bringin=False, antes=False):
        """
        Initialize the Blinds object with a given blind structure.
        """
        self.blinds = blinds
        self.bringin = bringin
        self.antes = antes

        if bringin:
            # We won't allow setting both blinds and bringin.
            # Bringin will take priority and trigger antes.
            self.antes = True

        self.SMBET, self.BB, self.SB, self.BRINGIN, self.ANTE = 0, 0, 0, 0, 0
        self.set_level(level)

    def fmtnum(self, num):
        if num % 1 > 0:
            return '{:.2f}'.format(num)
        else:
            return '{}'.format(int(num))

    def __str__(self):
        """
        Returns the stakes, as in the small bet/big bet amounts.
        Note: For ante/bringin games, the small-bet is SB and the big-bet is BB.
        """
        _str = ''
        if self.ANTE:
            _str += 'Ante: ${}, '.format(self.fmtnum(self.ANTE))

        if self.BRINGIN:
            _str += 'Bringin: ${}\n'.format(self.fmtnum(self.BRINGIN))
        if self.SB != self.BB:
            _str += 'SB: ${}, BB: ${}\n'.format(self.fmtnum(self.SB), self.fmtnum(self.BB))
        return _str

    def stakes(self, lvl=None):
        """
        Returns the stakes, as in the small bet/big bet amounts. For games that only use blinds
        (without antes), we calculate the amounts by using the Big Blind as the small bet, and
        twice the Big Blind as the big bet.
        """
        return '${}/${}'.format(self.BB, self.BB * 2)

    def cleannum(self, num):
        if num % 1 > 0:
            return num
        else:
            return int(num)

    def set_level(self, level):
        """
        Set the blind level, if valid.
        Default to regular blinds only.
        """
        if level not in stakes.keys():
            raise ValueError('level is out of bounds!')

        self.level = level
        self.SMBET = stakes[level]

        if self.blinds:
            self.SB, self.BB = self.cleannum(stakes[level] / 2), stakes[level]

        if self.bringin:
            self.BRINGIN = self.cleannum(stakes[level] / 2)

        if self.antes:
            self.ANTE = self.cleannum(stakes[level] / 4)

    def big_blinds(self, stack):
        """
        Returns how many big blinds are in the stack. Uses the Big Blind from the current level
        and rounds down.
        """
        return round_number(stack / self.BB)

    def trueBB(self, players):
        """
        Calculates the effective BB given how many players are at the table. When antes come
        into play it changes how much each hand costs.
        """
        if self.ANTE == 0:
            return self.BB
        pot = self.SB + self.BB + (players * self.ANTE)
        return round(pot * .66)

    def effectiveBB(self, stack, players):
        """
        Returns how many big blinds are effectively in the stack. First adds up the current pot
        which is (SB + BB + Antes). The players variable is an integer which specified how many
        antes to add. Then the effective big blind is 2/3rds of the pot. Returns a rounded
        integer.
        """
        return round_number(stack / self.trueBB(players))

    def sb_to_ante_ratio(self):
        """
        Returns the SB-to-Ante ratio of the current small blind and ante.
        """
        # Use only one decimal place.
        if self.ANTE > 0:
            return round(self.SB / self.ANTE, 1)
        else:
            return 0


def round_number(num):
    if num % 1 >= 0.5:
        return math.ceil(num)
    else:
        return math.floor(num)

"""
Stakes as listed out by big blind(or small bet)
"""
stakes = {
    1: 2,
    2: 4,
    3: 8,
    4: 15,
    5: 30,
    6: 50,
    7: 100,
    8: 200,
    9: 500,
    10: 1000,
}


def get_stakes(lev):
    return '${}/${}'.format(stakes[lev], stakes[lev]*2)


def levels(bet_dict=stakes):
    """
    Returns a listing of all the available blind levels in the structure.
    """
    for k, v in sorted(bet_dict):
        print('\tLevel {:3}: ${}/${}'.format(k, v, v * 2))
