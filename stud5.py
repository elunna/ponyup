#!/usr/bin/env python3

from __future__ import print_function
import os
import game
import blinds


class Stud5Game(game.Game):
    def play(self):
        """ Defines the structure of a hand played in the game."""
        newround = game.Round(self)
        newround.cheat_check()

        # Post antes

        # Show table pre draw
        print(newround)
        print(self._table)

        for street in range(4):
            if street == 0:
                # Five card stud - deal 2 cards to each player
                # 1 up and 1 down
                newround.deal_cards(1)
                newround.deal_cards(1, faceup=True)
            else:
                newround.deal_cards(1, faceup=True)

            newround.setup_betting()
            victor = newround.betting()

            if victor is not None:
                newround.award_pot(victor, newround.pot)
                break
        else:
            # Check for winners/showdown
            newround.showdown()

        # ================== CLEANUP
        newround.muck_all_cards()
        # Remove broke players
        newround.remove_broke_players()

        # Advance round counter
        self.rounds += 1


def main():
    os.system('clear')
    print('FIVE CARD STUD!')
    #  print('Initializing new game...\n')
    STAKES = blinds.limit['50/100']
    g = Stud5Game('FIVE CARD STUD', STAKES, 6, 'LUNNA')

    playing = True

    while playing:
        print(g)
        g.play()
        choice = input('keep playing? > ')
        if choice.lower() == 'n' or choice == 0:
            playing = False

        os.system('clear')
    exit()


if __name__ == "__main__":
    main()
