import session
import game


class Draw5Session(session.Session):
    def play(self):
        """ Defines the structure of a hand played in the game."""
        _round = game.Round(self)

        if len(self._table.get_cardholders()) > 0:
            raise Exception('One or more players have cards before the deal!')

        # todo: Postblinds
        _round.post_blinds()

        # A simple 1-bet
        #  newround.ante_up()

        # Five card draw - deal 5 cards to each player
        _round.deal_cards(5)

        # Show table pre draw
        print(_round)
        print(self._table)

        # Pre-draw betting round
        _round.setup_betting()
        victor = _round.betting()

        if victor is None:
            _round.muck.extend(game.discard_phase(self._table, _round.d))

            # Show table post draw
            print(self._table)

            # Post-draw betting round
            _round.setup_betting()
            victor = _round.betting()

            if victor is None:
                # Check for winners/showdown
                award_dict = _round.showdown()
            else:
                winner = _round._table.get_cardholders()
                award_dict = _round.split_pot(winner, _round.pot)
        else:
            winner = _round._table.get_cardholders()
            award_dict = _round.split_pot(winner, _round.pot)

        # Award pot
        for plyr, amt in award_dict.items():
            _round.award_pot(plyr, int(amt))

        # ================== CLEANUP
        # Cleanup all cards
        _round.muck_all_cards()
        _round.verify_muck()

        # Remove broke players
        _round._table.remove_broke()

        # Move the table button
        self._table.move_button()

        # Advance round counter
        self.rounds += 1
