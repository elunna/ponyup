import card
import evaluator


def bringin(table):
    """
    Finds which player has the lowest showing card and returns that player.
    """
    index = -1

    # Start with the lowest as the highest possible card to beat.
    lowcard = card.Card('Z', 's')
    seat = None

    for s in table:
        c = s.hand.cards[index]

        if c.rank < lowcard.rank:
            lowcard, seat = c, s
        elif c.rank == lowcard.rank:
            if card.SUITVALUES[c.suit] < card.SUITVALUES[lowcard.suit]:
                lowcard, seat = c, s
    return seat.NUM


def highhand(table, gametype):
    """
    Finds which player has the highest showing hand and return their seat index.  For stud
    games, after the first street, the high hand on board initiates the action (a tie is broken
    by position, with the player who received cards first acting first).
    """
    if gametype == 'SEVEN CARD STUD':
        up_start = 2
    elif gametype == 'FIVE CARD STUD':
        up_start = 1

    highvalue = 0
    seat = None
    ties = []

    for s in table.get_players(hascards=True):
        h = s.hand.cards[up_start:]
        value = evaluator.get_value(h)

        if value > highvalue:
            highvalue, seat = value, s
            ties = [seat]  # Reset any lower ties.
        elif value == highvalue:
            ties.append(s)
            if seat not in ties:
                ties.append(seat)

    # Return the seat index of the first-to-act.
    if len(ties) > 1:
        # Process ties, get the player who was dealt first.
        for s in table.get_players(hascards=True):
            if s in ties:
                return s.NUM
    else:
        return seat.NUM


def post_bringin(_round):
    """
    Gets the player who must post the bringin amount, adds their bet to the pot, and
    returns a string describing what the blinds posted.
    """
    table = _round._table
    bringin_index = bringin(table)
    table.set_bringin(bringin_index)
    seat = table.seats[bringin_index]

    # Set the BI token on the table.
    #  self._table.TOKENS['BI'] = self._table.get_index(bringin_index)

    # Bet the Bringin amount and add to the pot
    _round.pot += seat.bet(_round.blinds.BRINGIN)
    action = ''
    action += '{} brings it in for ${}\n'.format(seat.player, _round.blinds.BRINGIN)
    return action
