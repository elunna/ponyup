import ranges
import pokerhands


strat = {
    'FISH': {
        1: ranges.Ranges(
            call1=0,
            call2=pokerhands.PAIR_66,
            bet=0,
            raise1=pokerhands.PAIR_AA,
            raise2=pokerhands.PAIR_AA,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=pokerhands.PAIR_22,
            call2=pokerhands.PAIR_JJ,
            bet=pokerhands.TWOPAIR_22,
            raise1=pokerhands.TWOPAIR_JJ,
            raise2=pokerhands.TRIPS,
            bluff=0
        ),
        3: ranges.Ranges(
            call1=pokerhands.PAIR_22,
            call2=pokerhands.PAIR_JJ,
            bet=pokerhands.TWOPAIR_22,
            raise1=pokerhands.TWOPAIR_JJ,
            raise2=pokerhands.TRIPS,
            bluff=0
        ),
        4: ranges.Ranges(
            call1=pokerhands.PAIR_22,
            call2=pokerhands.PAIR_JJ,
            bet=pokerhands.TWOPAIR_22,
            raise1=pokerhands.TWOPAIR_JJ,
            raise2=pokerhands.TRIPS,
            bluff=0
        ),

    },

    'JACKAL': {
        1: ranges.Ranges(
            call1=pokerhands.HI_KT,
            call2=pokerhands.PAIR_66,
            bet=0,
            raise1=pokerhands.PAIR_66,
            raise2=pokerhands.PAIR_AA,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=pokerhands.PAIR_JJ,
            call2=pokerhands.PAIR_AA,
            bet=pokerhands.PAIR_66,
            raise1=pokerhands.TWOPAIR_TT,
            raise2=pokerhands.TWOPAIR_KK,
            bluff=0
        ),
        3: ranges.Ranges(
            call1=pokerhands.PAIR_JJ,
            call2=pokerhands.PAIR_AA,
            bet=pokerhands.PAIR_66,
            raise1=pokerhands.TWOPAIR_TT,
            raise2=pokerhands.TWOPAIR_KK,
            bluff=0
        ),
        4: ranges.Ranges(
            call1=pokerhands.PAIR_JJ,
            call2=pokerhands.PAIR_AA,
            bet=pokerhands.PAIR_66,
            raise1=pokerhands.TWOPAIR_TT,
            raise2=pokerhands.TWOPAIR_KK,
            bluff=0
        ),
    },

    'MOUSE': {
        1: ranges.Ranges(
            call1=pokerhands.TWOPAIR_KK,
            call2=pokerhands.TWOPAIR_TT,
            bet=0,
            raise1=pokerhands.TRIPS,
            raise2=pokerhands.STRAIGHT,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=pokerhands.TWOPAIR_TT,
            call2=pokerhands.TRIPS,
            bet=pokerhands.TWOPAIR_TT,
            raise1=pokerhands.STRAIGHT,
            raise2=pokerhands.FLUSH,
            bluff=0
        ),
        3: ranges.Ranges(
            call1=pokerhands.TWOPAIR_TT,
            call2=pokerhands.TRIPS,
            bet=pokerhands.TWOPAIR_TT,
            raise1=pokerhands.STRAIGHT,
            raise2=pokerhands.FLUSH,
            bluff=0
        ),
        4: ranges.Ranges(
            call1=pokerhands.TWOPAIR_TT,
            call2=pokerhands.TRIPS,
            bet=pokerhands.TWOPAIR_TT,
            raise1=pokerhands.STRAIGHT,
            raise2=pokerhands.FLUSH,
            bluff=0
        ),
    },

    'LION': {
        1: ranges.Ranges(
            call1=pokerhands.PAIR_88,
            call2=pokerhands.PAIR_KK,
            bet=0,
            raise1=pokerhands.PAIR_JJ,
            raise2=pokerhands.TRIPS,
            bluff=0
        ),
        2: ranges.Ranges(
            call1=pokerhands.TWOPAIR_TT,
            call2=pokerhands.TRIPS,
            bet=pokerhands.PAIR_KK,
            raise1=pokerhands.TRIPS,
            raise2=pokerhands.STRAIGHT,
            bluff=0
        ),
        3: ranges.Ranges(
            call1=pokerhands.TWOPAIR_TT,
            call2=pokerhands.TRIPS,
            bet=pokerhands.PAIR_KK,
            raise1=pokerhands.TRIPS,
            raise2=pokerhands.STRAIGHT,
            bluff=0
        ),
        4: ranges.Ranges(
            call1=pokerhands.TWOPAIR_TT,
            call2=pokerhands.TRIPS,
            bet=pokerhands.PAIR_KK,
            raise1=pokerhands.TRIPS,
            raise2=pokerhands.STRAIGHT,
            bluff=0
        ),
    }
}
