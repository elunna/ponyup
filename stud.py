from __future__ import print_function
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
                bring = self.r.bringin(r._table)
                print('Bringin is {}'.format(bring))

            else:
                r.deal_cards(1, faceup=True)
                high = self.r.highhand(r._table)
                if len(high) > 1:
                    print('There is a tie for high hand, going with {}'.format(high[0]))
                else:
                    print('Seat {} has the high hand and will act first.')

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
