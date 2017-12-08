from . import card


def set_bringin(self):
    """ Finds which player has the lowest showing card and sets that player
        to the bringin. Also sets the button the player to the right. If
        reverse is true, we find the highest card instead.
    """
    _seat = None
    lowcard = card.Card('Z', 's')  # Start high

    for s in self.get_players(hascards=True):
        c = s.hand.get_upcards()[0]
        if c.rank < lowcard.rank:
            lowcard, _seat = c, s
        elif c.rank == lowcard.rank:
            if card.SUITVALUES[c.suit] < card.SUITVALUES[lowcard.suit]:
                lowcard, _seat = c, s

    self.TOKENS['BI'] = _seat.NUM
    self.TOKENS['D'] = self.next_player(self.TOKENS['BI'], -1)

    return '{} has the lowest showing card.'.format(_seat.player)
