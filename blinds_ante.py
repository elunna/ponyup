import blinds


class BlindsAnte(blinds.Blinds):
    def __init__(self, level=1):
        super().__init__(level, structure_dict=ante)

# Since there is no Big Blind in these games, the BB represents the "Big Bet", and the SB
# represents the "Small Bet".
ante = {
    1:  (2, 1, 0.50, 0.25),
    2:  (4, 2, 1, .50),
    3:  (6, 3, 1.50, 0.75),
    4:  (8, 4, 2, 1),
    5:  (10, 5, 2.50, 1.25),
    6:  (12, 6, 3, 1.5),
    7:  (16, 8, 2, 1),
    8:  (30, 15, 6, 3),
    9:  (40, 20, 5, 10),
    10: (50, 25, 10, 5),
    11: (100, 50, 20, 10),
    12: (200, 100, 40, 20),
}
