import discard
import poker

DISPLAYWIDTH = 70
GAMES = {
    #  'OMAHA': [1, 1, 2, 2],
    #  'HOLDEM': [1, 1, 2, 2],
    'FIVE CARD DRAW': [1, 2],
    'FIVE CARD STUD': [1, 1, 2, 2],
    #  'SEVEN CARD STUD': [1, 1, 2, 2, 2],
}


class Session():
    """
    The Session object manages the general structure of a poker game. It sets up the essentials:
        game type, the table, and stakes.
    """
    def __init__(self, gametype, table, blinds):
        """
        Initialize the poker Session settings.
        """
        self.gametype = gametype
        self.rounds = 1
        self._table = table
        self.streets = GAMES[gametype]
        self.blinds = blinds

    def __str__(self):
        """
        Returns the Session info.
        """
        _str = 'Round: {:<5}\n'.format(self.rounds)
        stakes = 'Stakes: {}'.format(self.blinds)
        _str += stakes.rjust(DISPLAYWIDTH)

        return _str

    def new_round(self):
        return poker.Round(self)

    def play(self):
        """
        Defines the structure of how a single hand in the poker game is played.
        """
        print('Stub play function')


class Stud5Session(Session):
    def play(self):
        """
        Play a round of Five Card Draw.
        """
        r = self.new_round()
        r.check_integrity_pre()
        r.post_antes()

        for s in self.streets:
            if r.street == 0:
                # 1 face down, 1 up
                r.deal_cards(1)
                r.deal_cards(1, faceup=True)

                # The bringin determines the first bettor.
                bring = poker.bringin(r._table)
                print('Bringin is {}'.format(bring))

            else:
                r.deal_cards(1, faceup=True)
                high = poker.highhand(r._table, r.gametype)

                if len(high) > 1:
                    print('There is a tie for high hand, going with {}'.format(high[0]))
                else:
                    print('Seat {} has the high hand and will act first.')

            print(self._table)
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


class Draw5Session(Session):
    def play(self):
        """
        Play a round of Five Card Draw.
        """
        DEALT = 5
        r = self.new_round()
        r.check_integrity_pre()
        r.post_blinds()
        r.deal_cards(DEALT)
        r.sortcards()

        for s in self.streets:
            print(self._table)
            if r.street == 1:
                # Discard phase
                discards = discard.discard_phase(self._table, r.d)
                r.muck.extend(discards)
                r.sortcards()
                # print table after discarding and drawing
                print(self._table)

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
        self._table.move_button()
        self.rounds += 1
