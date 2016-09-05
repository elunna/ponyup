import blinds
import deck
import sessions
import pokerhands
import table_factory


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
    table = table_factory.Draw5Table(players)
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
