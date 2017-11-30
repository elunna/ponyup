"""
  " Manages a Draw Five Poker session.
  """
from ponyup import blinds
from ponyup import sessions
from ponyup import discard


class Draw5Session(sessions.Session):
    """ Five Card Draw poker session """
    def __init__(self):
        super().__init__(gametype="FIVE CARD DRAW")
        self.blinds = blinds.Blinds()

    def play(self):
        """ Play a round of Five Card Draw. """
        DEALT = 5
        self.table.move_button()
        r = self.new_round()
        r.setup()

        r.deal_cards(DEALT)
        r.sortcards()
        r.log_holecards()

        for _ in self.streets:
            if r.street == 1:
                discard.discard_phase(r)
                r.sortcards()
                r.log_holecards()

            if not r.betting_over():
                r.betting_round()

            if r.found_winner():
                break

        else:
            r.showdown()

        r.cleanup()
        self.rounds += 1
