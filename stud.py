import card


def determine_bringin(self, table, gametype):
    # Finds which player has the lowest showing card and returns that player.
    suitvalues = {'c': 1, 'd': 2, 'h': 3, 's': 4}
    index = -1
    if gametype == "STUD5":
        index = 1
    if gametype == "STUD7":
        index = 2

    # Start with the lowest as the highest possible card to beat.
    lowcard = card.Card('Z', 's')
    player = None
    for p in self._table:
        c = p._hand.cards[index]
        if c.rank < lowcard.rank:
            lowcard, player = c, p
        elif c.rank == lowcard.rank:
            if suitvalues[c.suit] < suitvalues[lowcard.suit]:
                lowcard, player = c, p
    return player
