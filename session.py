#!/usr/bin/env python3
import os
import game
import table

STARTINGCHIPS = 1000


class Session():
    """
    The Game object manages the general structure of a poker game. It sets up the essentials:
        game type, the table, and stakes.  The play() method defines the structure of how a
        single hand in the poker game is played.
    """
    def __init__(self, gametype, structure, tablesize=6, hero=None):
        """
        Initialize the poker Game.
        """
        self.blinds = structure
        self.rounds = 1
        self._table = table.setup_table(tablesize, hero)
        self._table.randomize_button()

        for p in self._table:
            p.chips = STARTINGCHIPS

    def __str__(self):
        """
        Represents the game as the round # and the stakes level.
        """
        _str = 'Round: {:<5} '.format(self.rounds)
        _str += 'Stakes: {}'.format(self.blinds.__str__().rjust(36))

        return _str

    def play(self):
        print('Stub play function')


class Draw5Session(Session):
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


def main():
    os.system('clear')
    print('FIVE CARD DRAW!')
    # def __init__(self, gametype, structure, tablesize=6, hero=None):
    sesh = Draw5Session('FIVE CARD DRAW', 10, 6, 'LUNNA')

    playing = True

    while playing:
        print(sesh)
        sesh.play()
        choice = input('keep playing? > ')
        if choice.lower() == 'n' or choice == 0:
            playing = False

        os.system('clear')
    exit()
