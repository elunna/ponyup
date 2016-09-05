import blinds
from blinds import Level


class BlindsNoAnte(blinds.Blinds):
    def __init__(self, level=1):
        super().__init__(level, structure_dict=no_ante)


def noante_level(sb, bb):
    return Level(sb, bb, 0, 0)

no_ante = {
    #
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
