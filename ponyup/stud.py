from ponyup import blinds
from ponyup import sessions


class Stud5Session(sessions.Session):
    def __init__(self):
        super().__init__(gametype="FIVE CARD STUD")
        self.blinds = blinds.Blinds(bringin=True)

    def play(self):
        """
        Play a round of Five Card Draw.
        """
        r = self.new_round()
        print(self)
        print(r.post_antes())

        for s in self.streets:
            r.log(r.get_street().name, decorate=True, echo=False)
            if r.street == 0:
                # 1 face down, 1 up
                r.deal_cards(1)
                r.deal_cards(1, faceup=True)
                r.log_holecards()

                # The bringin determines the first bettor.
                r.table.set_bringin()
                print(r.post_bringin())
            else:
                r.deal_cards(1, faceup=True, handreq=True)
                high = r.table.highhand()

                print('{} has high hand and will act first.'.format(r.table.seats[high]))

            if not r.betting_over():
                r.betting_round()

            if r.found_winner():
                break
        else:
            r.showdown()

        r.cleanup()
        self.rounds += 1

        r.hh.write_to_file()