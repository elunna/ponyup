from __future__ import print_function
import card
import poker


class Stud5Game(poker.Session):
    def play(self):
        _round = self.new_round()

        # Post antes
        _round.post_antes()

        # Show table pre draw
        print(_round)

        # 1 face down, 1 up
        _round.deal_cards(1)
        _round.deal_cards(1, faceup=True)

        print(self._table)

        bringin = _round.determine_bringin('STUD5')
        print('Bringin is {}'.format(bringin))

        """
        for street in range(4):
            if street == 0:
                # Five card stud - deal 2 cards to each player
                # 1 up and 1 down
                newround.deal_cards(1)
                newround.deal_cards(1, faceup=True)
            else:
                newround.deal_cards(1, faceup=True)

            newround.setup_betting()
            victor = newround.betting()

            if victor is not None:
                newround.award_pot(victor, newround.pot)
                break
        else:
            # Check for winners/showdown
            newround.showdown()
        """

        # ================== CLEANUP
        _round.muck_all_cards()
        # Remove broke players
        _round.remove_broke_players()

        # Advance round counter
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


def highhand(table):
    """
    Finds which player has the highest showing hand and return their seat index.
    """
