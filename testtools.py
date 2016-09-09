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


def deal_5stud_test_hands(table):
    hands = []
    hands.append(pokerhands.convert_to_cards(['As', 'Ah']))
    hands.append(pokerhands.convert_to_cards(['Ks', 'Kh']))
    hands.append(pokerhands.convert_to_cards(['Qs', 'Qh']))
    hands.append(pokerhands.convert_to_cards(['Js', 'Jh']))
    hands.append(pokerhands.convert_to_cards(['Ts', 'Th']))
    hands.append(pokerhands.convert_to_cards(['9s', '9h']))
    for p in table:
        p.hand.cards = hands.pop(0)


def deal_list_to_table(table, cards, faceup=False):
    if faceup:
        for c in cards:
            c.hidden = False

    for s in table:
        s.hand.add(cards.pop(0))


def deal_stud5(table, matchingranks=0):
    # These cards are meant to be dealt face-down
    down = pokerhands.convert_to_cards(['As', 'Ks', 'Qs', 'Js', 'Ts', '9s', '2d', '3d', '4d',
                                        '2s', '3s', '4s'])
    deal_list_to_table(table, down)

    # These are the up-cards
    if matchingranks == 0:
        up = pokerhands.convert_to_cards(['Ah', 'Kh', 'Qh', 'Jh', 'Th', '9h'])
    elif matchingranks == 2:
        up = pokerhands.convert_to_cards(['5h', '5c', 'Qh', 'Jh', 'Th', '9h'])
    elif matchingranks == 3:
        up = pokerhands.convert_to_cards(['5s', '5c', 'Qh', 'Jh', '5d', '9h'])
    elif matchingranks == 4:
        up = pokerhands.convert_to_cards(['5s', '5c', 'Qh', 'Jh', '5d', '5h'])

    deal_list_to_table(table, up, faceup=True)


def draw5_session(level, players=6):
    """
    Create a table of 6 draw5 players with default starting stacks. Blinds are $1/$2.
    """
    STAKES = blinds.BlindsNoAnte()
    STAKES.set_level(level)
    table = table_factory.Draw5Table(players)
    return sessions.Draw5Session('FIVE CARD DRAW', table, STAKES)


def stud5_session(level, players=6):
    """
    Create a table of 6 draw5 players with default starting stacks. Blinds are $1/$2.
    """
    STAKES = blinds.BlindsAnte()
    STAKES.set_level(level)
    table = table_factory.Stud5Table(players)
    return sessions.Stud5Session('FIVE CARD STUD', table, STAKES)


def deal_hand_dict(table, hand_dict):
    for k, v in sorted(hand_dict.items()):
        if k > len(table) - 1:
            return
        table.seats[k].hand.cards = v


def deal_ranked_hands(table, _rev=False):
    hands = sorted(RANKEDHANDS.keys())
    for s in table:
        if _rev:
            s.hand.cards = RANKEDHANDS[hands.pop()]
        else:
            s.hand.cards = RANKEDHANDS[hands.pop(0)]


def deal_random_cards(table, qty=5):
    d = deck.Deck()

    for s in table:
        for i in range(qty):
            s.hand.add(d.deal())


def get_cards(qty):
    d, cards = deck.Deck(), []
    for i in range(qty):
        cards.append(d.deal())
    return cards
