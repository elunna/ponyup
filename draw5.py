import sessions
import discard


class Draw5Session(sessions.Session):
    def play(self):
        """
        Play a round of Five Card Draw.
        """
        DEALT = 5
        self._table.move_button()
        r = self.new_round()
        print(self)

        r.hh.button()
        r._table.set_blinds()
        print(r.post_blinds())
        r.deal_cards(DEALT)
        r.sortcards()
        r.log_holecards()

        for s in self.streets:
            if r.street == 1:
                discard.discard_phase(r)
                r.sortcards()
                r.log_holecards()

            r.log(r.get_street().name, echo=False, decorate=True)

            if not r.betting_over():
                r.betting_round()

            if r.found_winner():
                break

        else:
            r.showdown()

        r.cleanup()
        self.rounds += 1

        # Write handhistory to file
        r.hh.write_to_file()
