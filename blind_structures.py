import blinds
from blinds import noante_level


class BlindsNoAnte(blinds.Blinds):
    def __init__(self, level=1):
        super().__init__(level, structure_dict=no_ante)


no_ante = {
    #
    1:  noante_level(2, 1),
    2:  noante_level(3, 1),
    3:  noante_level(4, 2),
    4:  noante_level(6, 3),
    5:  noante_level(8, 4),
    6:  noante_level(15, 10),
    7:  noante_level(20, 10),
    8:  noante_level(30, 15),
    9:  noante_level(50, 25),
    10: noante_level(100, 50),
}
