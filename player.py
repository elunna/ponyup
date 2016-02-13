import re
import hand
import strategy


class Player():
    def __init__(self, name, _type=None, chips=1000):
        if isValidUsername(name):
            self.name = name
        else:
            raise ValueError('Invalid username "{}" for object!'.format(name))

        if _type is None:
            self.playertype = 'CPU'
        elif _type != 'HUMAN' and _type != 'CPU':
            raise ValueError('Invalid player type passed!')
        else:
            self.playertype = _type

        if self.playertype == 'CPU':
            self.strategy = strategy.get_normal()

        self.chips = chips
        self._hand = hand.Hand()

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return str(self)

    def bet(self, bet):
        if bet > self.chips:
            # Put the player all-in
            bet = self.chips
            self.chips = 0
            return bet
        else:
            self.chips -= bet
            return bet

    def win(self, amt):
        self.chips += amt

    def showhand(self):
        self._hand.unhide()

    def fold(self):
        copy = self._hand.cards[:]
        self._hand.cards = []
        return copy

    # hand management
    def add(self, card):
        # Make sure we can see the card! (if we're human...)
        if self.playertype == 'HUMAN':
            card.hidden = False
        self._hand.add(card)

    def discard(self, card):
        # Test if the card is actually in the hand
        if card not in self._hand.cards:
            raise ValueError('Card not in players hand!')
        else:
            return self._hand.discard(card)

    def makeplay(self, options):
        return self.strategy.makeplay(options, self._hand.value)


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
    print('betting {}'.format(p.bet(100)))

    print('lunatunez stack = {}'.format(p.chips))
    print('Won {}'.format(p.win(500)))

    print('lunatunez stack = {}'.format(p.chips))
    print('betting {}'.format(p.win(100)))

    print('lunatunez stack = {}'.format(p.chips))

    print('betting {}'.format(p.bet(1000)))

    print('lunatunez stack = {}'.format(p.chips))
    print('')
    print('Attempting to bet 1000')
    print('betting {}'.format(p.bet(1000)))

    print('lunatunez stack = {}'.format(p.chips))
