from ponyup import blinds
from ponyup import sessions


class PokerSession(sessions.Session):
    def __init__(self):
        super().__init__(gametype="POKER")
        self.blinds = blinds.Blinds(bringin=True)

    def play(self):
        """
        Deals out 5 card poker.
        """
        r = self.new_round()
        DEALT = 5
        r.deal_cards(DEALT)
        print(self)

        for s in self.streets:
            r.betting_round()
        print(r.showdown())

        r.cleanup()
        self.rounds += 1
