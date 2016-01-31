import re


class Player():
    def __init__(self, name, _type=None, chips=1000):
        if isValidUsername(name):
            self.name = name
        else:
            raise ValueError('Invalid username "{}" for object!'.format(name))

        if _type is not None:
            self.playertype = _type
        else:
            self.playertype = 'Unknown'

        self.chips = chips

        # Should we have any hand management?
        self.hand = None

    def __str__(self):
        #  print('{} -- a {}'.format(self.name, self.playertype))
        return '{}'.format(self.name)

    def bet(self, bet):
        if bet > self.chips:
            print('Invalid bet amount - more than player has!')
            raise ValueError()
            return -1
        else:
            self.chips -= bet
            return bet

    def win(self, amt):
        self.chips += amt


def isValidUsername(username):
    re1 = re.compile(r"[<>/{}[\]~`^'\\]")
    if re1.search(username):
        #  print ("RE1: Invalid char detected.")
        return False
    else:
        #  print ("RE1: No invalid char detected.")
        return True


def test_newplayer(name):
    try:
        p = Player(name)
        print(p)
        print('')
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    test_newplayer('Erik')
    test_newplayer('Erik!')
    test_newplayer('Erik@')
    test_newplayer('Erik#')
    test_newplayer('Erik$')
    test_newplayer('Erik%')
    test_newplayer('Erik^')
    test_newplayer('Erik&')
    test_newplayer('Erik*')
    test_newplayer('Erik(')
    test_newplayer('Erik)')
    test_newplayer('Erik[')
    test_newplayer('Erik]')
    test_newplayer('Erik{')
    test_newplayer('Erik}')
    test_newplayer('Erik;')
    test_newplayer('Erik:')
    test_newplayer('Erik\'')
    test_newplayer('Erik-')
    test_newplayer('Erik_')
    test_newplayer('Erik=')
    test_newplayer('Erik+')
    test_newplayer('Erik|')
    test_newplayer('Erik\\')
    test_newplayer('Erik/')
    test_newplayer('Erik?')
    test_newplayer('Erik.')
    test_newplayer('Erik,')
    test_newplayer('Erik<')
    test_newplayer('Erik>')

    print('#'*80)
    p = Player('lunatunez')
    print(p)
    print('lunatunez stack = {}'.format(p.chips))
    print('betting 100')
    p.bet(100)
    print('lunatunez stack = {}'.format(p.chips))
    print('Won 500')
    p.win(500)
    print('lunatunez stack = {}'.format(p.chips))
    print('betting 100')
    p.win(100)
    print('lunatunez stack = {}'.format(p.chips))
