import blinds
from blinds import Level


class BlindsAnte(blinds.Blinds):
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
