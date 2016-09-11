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
        r._table.set_blinds()
        r.out(r.post_blinds())  # Log this
        r.deal_cards(DEALT)
        r.out('HOLE CARDS', decorate=True)
        r.out('Dealt to {}: [{}]'.format(r.hero.player, r.hero.hand.peek()))
        r.sortcards()

        for s in self.streets:
            if r.street == 1:
                # Discard phase
                discard.discard_phase(r)
                r.sortcards()
                # print table after discarding and drawing

            if not r.betting_over():
                r.betting_round()

            if r.found_winner():
                break
        else:
            r.showdown()

        r.cleanup()
        self.rounds += 1
