from __future__ import print_function
import card
import evaluator
import poker


class Stud5Session(poker.Session):
    def play(self):
        """
        Play a round of Five Card Draw.
        """
        r = self.new_round()
        r.check_integrity_pre()
        r.post_antes()

        for s in self.streets:
            print(self._table)
            if r.street == 0:
                # 1 face down, 1 up
                r.deal_cards(1)
                r.deal_cards(1, faceup=True)

                # The bringin determines the first bettor.
                utg = r.determine_bringin()
                print('Bringin is {}'.format(bringin))

            else:
                r.deal_cards(1, faceup=True)

            victor = r.betting_round()
            print(r)           # Display pot

            if victor is None:
                r.next_street()
            else:
                # One player left, award them the pot!
                r.award_pot(victor, r.pot)
                break
        else:
            r.showdown()

        r.cleanup()
        self.rounds += 1


def bringin(table):
    """
    Finds which player has the lowest showing card and returns that player.
    """
    index = -1

    # Start with the lowest as the highest possible card to beat.
    lowcard = card.Card('Z', 's')
    # Make sure
    player = None
    for p in table:
        c = p._hand.cards[index]

        if c.rank < lowcard.rank:
            lowcard, player = c, p
        elif c.rank == lowcard.rank:
            if card.SUITVALUES[c.suit] < card.SUITVALUES[lowcard.suit]:
                lowcard, player = c, p
    return table.get_index(player)


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
    player = None
    ties = []

    for p in table:
        h = p._hand.cards[up_start:]
        value = evaluator.get_value(h)

        if value > highvalue:
            highvalue, player = value, p
            ties = []  # Reset any lower ties.
        elif value == highvalue:
            ties.append(p)
            if player not in ties:
                ties.append(player)

    if ties:
        return sorted([table.get_index(p) for p in ties])
    else:
        return table.get_index(player)
