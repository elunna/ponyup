import sessions
import stud


class Stud5Session(sessions.Session):
    def play(self):
        """
        Play a round of Five Card Draw.
        """
        r = self.new_round()
        print(r.post_antes())

        for s in self.streets:
            r.log(r.get_street().name, decorate=True)
            if r.street == 0:
                # 1 face down, 1 up
                r.deal_cards(1)
                r.deal_cards(1, faceup=True)
                r.hh.log_holecards()

                # The bringin determines the first bettor.
                r._table.set_bringin()
                print(r.post_bringin())
            else:
                r.deal_cards(1, faceup=True, handreq=True)
                high = stud.highhand(r._table)

                print('{} has high hand and will act first.'.format(r._table.seats[high]))

            if not r.betting_over():
                r.betting_round()

            if r.found_winner():
                break
        else:
            r.showdown()

        r.cleanup()
        self.rounds += 1

        r.hh.write_to_file('logs/stud5.log')
