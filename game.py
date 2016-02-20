import table
import draw5
import gameround


class Game():
    """
    The Game object manages the general structure of a poker game. It sets up the
    essentials: game type, the table, and stakes.
    The play() method defines the structure of how a single hand in the poker game is
    played.
    """

    def __init__(self, gametype, stakes, tablesize=6, hero=None):
        """ Initialize the poker Game. """
        #  self.blinds = blinds.limit[stakes]
        self.blinds = stakes
        self.rounds = 1
        self._table = table.setup_table(tablesize, hero)
        self._table.randomize_button()

    def __str__(self):
        """ Represents the game as the round # and the stakes level."""
        _str = 'Round: {:<5} '.format(self.rounds)
        _str += 'Stakes: ${}/${}'.format(
            self.blinds[1], self.blinds[1] * 2).rjust(36)

        return _str

    def play(self):
        """ Defines the structure of a hand played in the game."""
        newround = gameround.Round(self)
        newround.cheat_check()

        # todo: Postblinds
        newround.post_blinds()

        # A simple 1-bet
        #  newround.ante_up()

        # Five card draw - deal 5 cards to each player
        newround.deal_hands(5)

        # Show table pre draw
        print(newround)
        print(self._table)

        # Pre-draw betting round
        newround.setup_betting()
        victor = newround.betting()

        if victor is None:
            #  newround.discard_phase()
            newround.muck.extend(draw5.discard_phase(self._table, newround.d))

            # Show table post draw
            print(self._table)

            # Post-draw betting round
            newround.setup_betting()
            victor = newround.betting()

            if victor is None:
                # Check for winners/showdown
                newround.showdown()

                # Award pot
            else:
                newround.award_pot(victor, newround.pot)
        else:
            newround.award_pot(victor, newround.pot)

        # ================== CLEANUP
        newround.check_muck()

        # Move the table button
        self._table.move_button()

        # Advance round counter
        self.rounds += 1
