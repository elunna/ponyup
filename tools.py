import card
import deck

# These are constants to help with computer AI
HI_9x = 900
HI_Jx = 1100
HI_Ax = 1400
HI_Axx = 140000
HI_Kxx = 130000
HI_Txx = 100000
HI_Axxx = 14000000
HI_Kxxx = 13000000
HI_KT = 1310000000
HI_AQ = 1412000000
HI_Axxxx = 1400000000
PAIR_22 = 20000000000
PAIR_66 = 20600000000
PAIR_88 = 20800000000
PAIR_JJ = 21100000000
PAIR_KK = 21300000000
PAIR_AA = 21400000000
TWOPAIR_22 = 30000000000
TWOPAIR_88 = 30800000000
TWOPAIR_TT = 31000000000
TWOPAIR_JJ = 31100000000
TWOPAIR_KK = 31300000000
TRIPS = 40000000000
STRAIGHT = 40000000000
FLUSH = 50000000000

HANDS = {
    'dupes': ['As', '3h', 'As', '4d', '5c'],
    'royalflush': ['As', 'Ks', 'Js', 'Ts', 'Qs'],
    'straightflush_high': ['9s', 'Ks', 'Qs', 'Js', 'Ts'],
    'straightflush 4card': ['Ks', 'Qs', 'Js', 'Ts'],
    'straightflush_low': ['2s', 'As', '3s', '4s', '5s'],
    'quads_high': ['As', 'Ad', 'Ah', 'Ac', 'Kc'],
    'quads_low': ['2s', '2d', '2h', '2c', '3c'],
    'fullhouse_high': ['As', 'Ad', 'Ah', 'Kd', 'Kc'],
    'fullhouse_low': ['2s', '2d', '2h', '3d', '3c'],
    'flush_high': ['As', 'Ks', 'Qs', 'Js', '9s'],
    'flush_low': ['2s', '3s', '4s', '5s', '7s'],
    'straight_high': ['As', 'Tc', 'Ks', 'Jd', 'Qh'],
    'straight_mid': ['8s', '7h', '9s', 'Td', 'Jh'],
    'straight_low': ['2s', '3h', 'As', '4d', '5c'],
    'trips_high': ['As', 'Kh', 'Ah', 'Ad', 'Qc'],
    'trips_low': ['2s', '2h', '2h', '3d', '4c'],
    'twopair_high': ['As', 'Ah', 'Ks', 'Kd', 'Qc'],
    'twopair_low': ['2s', '2h', '3s', '3d', '4c'],
    'pair_high': ['Ks', 'Qh', 'As', 'Ad', 'Jc'],
    'pair_low': ['2s', '3h', '2c', '4d', '5c'],
    'OESFD': ['Js', 'Ts', '8s', '2d', '9s'],
    'GSSFD': ['Js', 'Ts', '7s', '2d', '9s'],
    'flushdrawA': ['As', 'Ts', '7s', '2d', '9s'],
    'flushdrawB': ['3s', 'Ts', '7s', '2d', '9s'],
    'flushdraw 4card': ['3s', 'Ts', '7s', '9s'],
    'OESD': ['Jh', 'Ts', '8c', '2d', '9s'],
    'OESD 4card': ['Jh', 'Ts', '8c', '9s'],
    'GSSD': ['Jh', 'Ts', 'As', '2d', 'Kh'],
    'wheeldraw': ['3h', '4s', 'As', '2d', 'Kh'],
    'BDFD1': ['2d', '4s', '5s', '7s', 'Kh'],
    'BDFD2': ['Ad', '4s', '5s', '7s', 'Kh'],
    'highcards': ['Ad', '4s', 'Qs', '7s', 'Kh'],
    'acehigh': ['Ad', '4s', '5s', '7s', '9h'],
    'BDSD1': ['2d', '7s', '8s', '9d', 'Kh'],
    'BDSD2': ['2d', '7s', '8s', 'Td', 'Kh'],
    'junk': ['2d', '3s', '6s', '8d', 'Th'],
    '2AA_v1': ['2s', 'As', 'Ah'],
    '2AA_v2': ['2c', 'Ad', 'Ac'],
    '2KK': ['2h', 'Ks', 'Kh'],
    '2QQ': ['2d', 'Qs', 'Qh'],
    '3AK_v1': ['3s', 'As', 'Ks'],
    '3AK_v2': ['3h', 'Ah', 'Kh'],
    '3AK_v3': ['3c', 'Ac', 'Kc'],
    'QKA_v1': ['Qs', 'Kh', 'As'],
    'QKA_v2': ['Qc', 'Ks', 'Ac'],
    'JTQ': ['Jh', 'Ts', 'Qh'],
    '234': ['3s', '4s', '5s'],
    '345': ['3d', '4d', '5d'],
    '245': ['2c', '4c', '5c'],
    '89J': ['8c', '9s', 'Js'],
    '567': ['5c', '6s', '7s'],
    'A': ['As'],
    'AKs': ['Ac', 'Kc'],
    'AKo': ['As', 'Kd'],
    'AA': ['Ac', 'Ah'],
    'KK_dupes': ['Ks', 'Ks'],
    'QQ': ['Qc', 'Qh'],
    '23': ['2c', '3h'],
}


def to_card(string):
    c = card.Card(*string)
    c.hidden = False
    return c


def convert_to_cards(strings):
    # Unhide for testing purposes
    cards = [to_card(x) for x in strings]
    return cards


def make(hand_name, hidden=False):
    h = convert_to_cards(HANDS[hand_name])
    if not hidden:
        for c in h:
            c.hidden = False
    return h


def deal_5stud_test_hands(table):
    hands = []
    hands.append(convert_to_cards(['As', 'Ah']))
    hands.append(convert_to_cards(['Ks', 'Kh']))
    hands.append(convert_to_cards(['Qs', 'Qh']))
    hands.append(convert_to_cards(['Js', 'Jh']))
    hands.append(convert_to_cards(['Ts', 'Th']))
    hands.append(convert_to_cards(['9s', '9h']))
    # This is 5 stud, so the cards after the first should be faceup.
    for h in hands:
        for c in h[1:]:
            c.hidden = False
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
    down = convert_to_cards(['As', 'Ks', 'Qs', 'Js', 'Ts', '9s', '2d', '3d', '4d',
                             '2s', '3s', '4s'])
    deal_list_to_table(table, down)

    # These are the up-cards
    if matchingranks == 0:
        up = convert_to_cards(['Ah', 'Kh', 'Qh', 'Jh', 'Th', '9h'])
    elif matchingranks == 2:
        up = convert_to_cards(['5h', '5c', 'Qh', 'Jh', 'Th', '9h'])
    elif matchingranks == 3:
        up = convert_to_cards(['5s', '5c', 'Qh', 'Jh', '5d', '9h'])
    elif matchingranks == 4:
        up = convert_to_cards(['5s', '5c', 'Qh', 'Jh', '5d', '5h'])

    deal_list_to_table(table, up, faceup=True)


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
        c = d.deal()
        c.hidden = False
        cards.append(c)
    return cards


RANKEDHANDS = {
    0: make('royalflush'),
    1: make('straightflush_high'),
    2: make('fullhouse_high'),
    3: make('flush_high'),
    4: make('straight_high'),
    5: make('trips_high'),
    6: make('twopair_high'),
    7: make('pair_high'),
    8: make('pair_low'),
    9: make('acehigh'),
}
