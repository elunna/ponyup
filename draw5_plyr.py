import ranges
import tools

strat = {
    'FISH': {
        1: ranges.Ranges(
            call1=0,
            call2=tools.PAIR_66,
            bet=0,
            raise1=tools.PAIR_AA,
            raise2=tools.PAIR_AA,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=tools.PAIR_22,
            call2=tools.PAIR_JJ,
            bet=tools.TWOPAIR_22,
            raise1=tools.TWOPAIR_JJ,
            raise2=tools.TRIPS,
            bluff=0
        ),
    },

    'JACKAL':  {
        1: ranges.Ranges(
            call1=tools.HI_KT,
            call2=tools.PAIR_66,
            bet=0,
            raise1=tools.PAIR_66,
            raise2=tools.PAIR_AA,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=tools.PAIR_JJ,
            call2=tools.PAIR_AA,
            bet=tools.PAIR_66,
            raise1=tools.TWOPAIR_TT,
            raise2=tools.TWOPAIR_KK,
            bluff=0
        ),
    },

    'MOUSE': {
        1: ranges.Ranges(
            call1=tools.PAIR_88,
            call2=tools.PAIR_KK,
            bet=0,
            raise1=tools.PAIR_AA,
            raise2=tools.TWOPAIR_JJ,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=tools.PAIR_KK,
            call2=tools.TWOPAIR_22,
            bet=tools.PAIR_KK,
            raise1=tools.TRIPS,
            raise2=tools.STRAIGHT,
            bluff=0
        ),
    },

    'LION': {
        1: ranges.Ranges(
            call1=tools.PAIR_88,
            call2=tools.PAIR_KK,
            bet=0,
            raise1=tools.PAIR_JJ,
            raise2=tools.TRIPS,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=tools.TWOPAIR_TT,
            call2=tools.TRIPS,
            bet=tools.PAIR_KK,
            raise1=tools.TRIPS,
            raise2=tools.STRAIGHT,
            bluff=0
        ),
    }
}
