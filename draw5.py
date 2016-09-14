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

        r.hh.button()
        r._table.set_blinds()
        r.log(r.post_blinds())  # Log this
        r.deal_cards(DEALT)
        r.hh.log_holecards()
        r.sortcards()

        for s in self.streets:
            if r.street == 1:
                discard.discard_phase(r)
                r.sortcards()

            r.log(r.get_street().name, decorate=True)
            if not r.betting_over():
                r.betting_round()

            if r.found_winner():
                break

        else:
            r.showdown()

        r.cleanup()
        self.rounds += 1

        # Write handhistory to file
        r.hh.write_to_file('logs/draw5.log')
