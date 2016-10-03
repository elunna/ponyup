from ponyup import holdem

SKLANSKY = {
    1: ['AA', 'KK', 'QQ', 'JJ', 'AKs'],
    2: ['TT', 'AK', 'AQs', 'AJs', 'KQs'],
    3: ['99', 'AQ', 'ATs', 'KJs', 'QJs', 'JTs'],
    4: ['88', 'AJ', 'KQ', 'KTs', 'QTs', 'J9s', 'T9s', '98s'],
    5: ['77', '66', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
        'KJ', 'QJ', 'JT', 'Q9s', 'T8s', '97s', '87s', '76s'],
    6: ['55', 'AT', 'KT', 'QT', 'J8s', '86s', '75s', '65s', '54s'],
    7: ['44', '33', '22', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s',
        'Q8s', 'T7s', 'J9', 'T9', '98', '64s', '53s', '43s'],
    8: ['A9', 'K9', 'Q9', 'J8', 'Q7s', 'J7s', 'T8', '96s', '87', '85s', '76', '74s',
        '65', '54', '42s', '32s'],
}


def get_group(cardrep):
    """
    Takes the text representation of a pair of hole cards and returns what Skylansky hand group
    they belong in. This doesn't take As Ks, it would take 'AKo'
    If the cards are not found in a group, returns -1

    If the card is 87 (8 7 offsuit), but comes in as 87o, this will cut out the 'o'
    """
    if isinstance(cardrep, list):
        cardrep = holdem.card2text(cardrep)

    if cardrep.endswith('o'):
        cardrep = cardrep[0:2]
    for k, v in SKLANSKY.items():
        if cardrep in v:
            return k
    else:
        return -1


def percentile(group):
    """
    Takes in a group number and returns what percent of playable hands that group represents.
    ie: Group 1 is about 5%
    """
    STARTINGHANDS = 1326
    hands = 0

    for i in range(1, group + 1):
        for h in SKLANSKY[i]:
            hands += len(holdem.text2cards(h))

    return int((hands / STARTINGHANDS) * 100)

if __name__ == "__main__":
    for k in sorted(SKLANSKY.keys()):
        print('Group {} is {}% of hands.'.format(k, percentile(k)))
