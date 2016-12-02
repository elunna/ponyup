"""
  " Strategies for Five Stud computer players
  """
from ponyup import ranges
from ponyup import tools


strat = {
    'FISH': {
        1: ranges.Ranges(
            call1=0,
            call2=tools.HI_9x,
            bet=tools.PAIR_88,
            raise1=tools.PAIR_88,
            raise2=tools.PAIR_KK,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=0,
            call2=tools.HI_Kxx,
            bet=tools.PAIR_88,
            raise1=tools.PAIR_JJ,
            raise2=tools.TRIPS,
            bluff=0
        ),
        3: ranges.Ranges(
            call1=tools.HI_Kxxx,
            call2=tools.PAIR_22,
            bet=tools.PAIR_JJ,
            raise1=tools.PAIR_AA,
            raise2=tools.TRIPS,
            bluff=0
        ),
        4: ranges.Ranges(
            call1=tools.HI_Axxxx,
            call2=tools.PAIR_22,
            bet=tools.PAIR_JJ,
            raise1=tools.TWOPAIR_JJ,
            raise2=tools.TRIPS,
            bluff=0
        ),

    },

    'JACKAL': {
        1: ranges.Ranges(
            call1=tools.HI_9x,
            call2=tools.PAIR_22,
            bet=tools.PAIR_22,
            raise1=tools.PAIR_22,
            raise2=tools.PAIR_88,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=tools.HI_Axx,
            call2=tools.PAIR_66,
            bet=tools.PAIR_22,
            raise1=tools.PAIR_88,
            raise2=tools.PAIR_88,
            bluff=0
        ),
        3: ranges.Ranges(
            call1=tools.PAIR_22,
            call2=tools.PAIR_66,
            bet=tools.PAIR_66,
            raise1=tools.PAIR_88,
            raise2=tools.PAIR_JJ,
            bluff=0
        ),
        4: ranges.Ranges(
            call1=tools.PAIR_22,
            call2=tools.PAIR_66,
            bet=tools.PAIR_88,
            raise1=tools.PAIR_JJ,
            raise2=tools.TWOPAIR_22,
            bluff=0
        ),

    },

    'MOUSE': {
        1: ranges.Ranges(
            call1=tools.PAIR_22,
            call2=tools.PAIR_88,
            bet=tools.PAIR_JJ,
            raise1=tools.PAIR_KK,
            raise2=tools.PAIR_AA,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=tools.PAIR_66,
            call2=tools.PAIR_88,
            bet=tools.PAIR_JJ,
            raise1=tools.PAIR_KK,
            raise2=tools.TRIPS,
            bluff=0
        ),
        3: ranges.Ranges(
            call1=tools.PAIR_66,
            call2=tools.PAIR_JJ,
            bet=tools.PAIR_KK,
            raise1=tools.TWOPAIR_22,
            raise2=tools.TRIPS,
            bluff=0
        ),
        4: ranges.Ranges(
            call1=tools.PAIR_88,
            call2=tools.PAIR_JJ,
            bet=tools.PAIR_KK,
            raise1=tools.TWOPAIR_22,
            raise2=tools.TRIPS,
            bluff=0
        ),
    },

    'LION': {
        1: ranges.Ranges(
            call1=tools.HI_9x,
            call2=tools.PAIR_22,
            bet=tools.PAIR_22,
            raise1=tools.PAIR_22,
            raise2=tools.PAIR_88,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=tools.HI_Axx,
            call2=tools.PAIR_66,
            bet=tools.PAIR_22,
            raise1=tools.PAIR_88,
            raise2=tools.PAIR_88,
            bluff=0
        ),
        3: ranges.Ranges(
            call1=tools.PAIR_22,
            call2=tools.PAIR_66,
            bet=tools.PAIR_66,
            raise1=tools.PAIR_88,
            raise2=tools.PAIR_JJ,
            bluff=0
        ),
        4: ranges.Ranges(
            call1=tools.PAIR_22,
            call2=tools.PAIR_66,
            bet=tools.PAIR_88,
            raise1=tools.PAIR_JJ,
            raise2=tools.TWOPAIR_22,
            bluff=0
        ),
    }
}
