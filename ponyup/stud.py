"""
  " Manages a Draw Five Poker session.
  """
from ponyup import blinds
from ponyup import poker
from ponyup import sessions


class Stud5Session(sessions.Session):
    """ Five Card Stud poker session """
    def __init__(self):
        super().__init__(gametype="FIVE CARD STUD")
        self.blinds = blinds.Blinds(blinds=False, antes=True, bringin=True)

    def new_round(self):
        r = poker.StudRound(self)
        r.log_hh()
        return r

    def play(self):
        """ Play a round of Five Card Draw. """
        r = self.new_round()
        r.setup()

        for _ in self.streets:
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
                high = r.highhand()

                print('{} has high hand and will act first.'.format(r.table.seats[high]))

            if not r.betting_over():
                r.betting_round()

            if r.found_winner():
                break
        else:
            print(r.showdown())

        r.cleanup()
        self.rounds += 1
