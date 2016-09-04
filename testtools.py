import blinds
import deck
import sessions
import names
import player
import pokerhands
import table

STARTINGCHIPS = 1000
STEP = 100


RANKEDHANDS = {
    0: pokerhands.make('royalflush'),
    1: pokerhands.make('straightflush_high'),
    2: pokerhands.make('fullhouse_high'),
    3: pokerhands.make('flush_high'),
    4: pokerhands.make('straight_high'),
    5: pokerhands.make('trips_high'),
    6: pokerhands.make('twopair_high'),
    7: pokerhands.make('pair_high'),
    8: pokerhands.make('pair_low'),
    9: pokerhands.make('acehigh'),
}


def deal_stud(table, qty, matchingranks=0):
    down = pokerhands.convert_to_cards(['As', 'Ks', 'Qs', 'Js', 'Ts', '9s',
                                        '2d', '3d', '4d', '2s', '3s', '4s'])
    if qty == 2:
        deal_list_to_table(table, down)
    elif qty == 3:
        deal_list_to_table(table, down)
        deal_list_to_table(table, down)
    else:
        raise Exception('bad qty!')

    if matchingranks == 0:
        up = pokerhands.convert_to_cards(['Ah', 'Kh', 'Qh', 'Jh', 'Th', '9h'])
    elif matchingranks == 2:
        up = pokerhands.convert_to_cards(['5h', '5c', 'Qh', 'Jh', 'Th', '9h'])
    elif matchingranks == 3:
        up = pokerhands.convert_to_cards(['5s', '5c', 'Qh', 'Jh', '5d', '9h'])
    elif matchingranks == 4:
        up = pokerhands.convert_to_cards(['5s', '5c', 'Qh', 'Jh', '5d', '5h'])
    else:
        raise Exception('bad matchingranks #, 0, 2, 3, or 4!')

    deal_list_to_table(table, up, faceup=True)


def draw5_session(level, players=6):
    """
    Create a table of 6 draw5 players with default starting stacks. Blinds are $1/$2.
    """
    STAKES = blinds.Blinds()
    STAKES.set_level(level)
    table = BobTable(players)
    return sessions.Draw5Session('FIVE CARD DRAW', table, STAKES)


def deal_hand_dict(table, hand_dict):
    for k, v in sorted(hand_dict.items()):
        if k > len(table) - 1:
            return
        table.seats[k]._hand.cards = v


def deal_ranked_hands(table, _rev=False):
    hands = sorted(RANKEDHANDS.keys())
    for s in table:
        if _rev:
            s._hand.cards = RANKEDHANDS[hands.pop()]
        else:
            s._hand.cards = RANKEDHANDS[hands.pop(0)]


def deal_random_cards(table, qty=5):
    d = deck.Deck()

    for p in table:
        for i in range(qty):
            p.add_card(d.deal())


def deal_list_to_table(table, cards, faceup=False):
    if faceup:
        for c in cards:
            c.hidden = False

    for p in table:
        p.add_card(cards.pop(0))


def get_cards(qty):
    d, cards = deck.Deck(), []
    for i in range(qty):
        cards.append(d.deal())
    return cards


class BobTable(table.Table):
    """
    Creates a table of bobs with the default chip stack.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            self.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
            self.seats[i].chips = STARTINGCHIPS


class SteppedStackTable(table.Table):
    """
    Creates a table of bobs with stack sizes starting from 100 and increasing in 100's for
    each seat.
    """
    def __init__(self, seats):
        super().__init__(seats)

        for i, s in enumerate(self.seats):
            self.add_player(i, player.Player('bob{}'.format(i), 'CPU'))
            self.seats[i].chips = STEP * (i + 1)


class HeroTable(table.Table):
    """
    Creates a table with the human hero player, and populates the table full of random named
    players. Each player has the default starting stack size.
    """
    def __init__(self, seats, hero):
        super().__init__(seats)

        nameset = names.random_names(seats)
        # Add the hero to seat 0
        self.add_player(0, player.Player(hero, 'HUMAN'))

        for i, s in enumerate(self.seats):
            if s is None:
                self.add_player(i, player.Player(nameset.pop(), "CPU"))
            else:
                nameset.pop()
            self.seats[i].chips = STARTINGCHIPS
