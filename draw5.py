#!/usr/bin/env python3

from __future__ import print_function
import pokerhands
import evaluator as ev
import cardlist
import hand
import card
import os
import game
import blinds


def is_integer(num):
    """ Determines if the variable is an integer"""
    try:
        int(num)
        return True
    except ValueError:
        return False


def discard_phase(table, deck):
    """
    Goes through a table and offers all players with cards the option to discard.
    Returns a list of all the discards (ie:"muck" cards)
    """
    print('\nDiscard phase...')
    # Make sure the button goes last!
    holdingcards = table.get_cardholders()
    muckpile = []

    for p in holdingcards:

        ishuman = p.playertype == 'HUMAN'
        # Discard!
        if ishuman:
            discards = human_discard(p._hand)
        else:
            discards = auto_discard(p._hand)

        if discards:
            # Easier to put this here...
            if ishuman:
                print('{:15} discards {}, draws: '.format(
                    str(p), discards), end='')
            else:
                print('{:15} discards {}.'.format(
                    str(p), discards), end='')
        else:
            print('{:15} stands pat.'.format(str(p)))

        # Redraw!
        for c in discards:
            muckpile.append(p.discard(c))

            draw = deck.deal()
            if ishuman:
                draw.hidden = False
                print('{} '.format(draw), end='')

            p.add(draw)
        print('')
    print('')

    return muckpile


def human_discard(hand):
    print('*'*40)
    print(' '*35 + '1  2  3  4  5')
    print(' '*35, end='')
    for c in hand.cards:
        print('{:3}'.format(str(c)), end='')
    print('')
    print('Enter the cards you want to discard:')
    print('Example: "1" discards card 1, "12" discards cards 1 and 2, etc.')
    print('')
    choice = input(':> ')
    # Split up the #s, and reverse them so we can remove them without the list
    # collapsing and disrupting the numbering.
    validnumbers = ['1', '2', '3', '4', '5']
    choice = sorted(list(choice), reverse=True)
    discards = []
    for c in choice:
        if is_integer(c) and c in validnumbers:
            discards.append(hand.cards[int(c) - 1])
        else:
            pass
    return discards


def auto_discard(hand):
    # hand is a Hand object

    # Obviously we will stand pat on:
    PAT_HANDS = ['STRAIGHT', 'FLUSH', 'FULL HOUSE', 'STRAIGHT FLUSH', 'ROYAL FLUSH']
    DIS_RANKS = ['PAIR', 'TRIPS', 'QUADS']
    discard = []

    h = cardlist.rank_list(hand.cards)

    if hand.handrank in PAT_HANDS:
        pass
    elif hand.handrank in DIS_RANKS:
        #  standard discard
        highcards = h[0][1]
        discard = cardlist.pop_ranks(hand.cards, highcards)
    elif hand.handrank == 'TWO PAIR':
        # Keep the twp pair, discard 1.
        highcards = h[0][1] + h[1][1]

        discard = cardlist.pop_ranks(hand.cards, highcards)

    elif hand.handrank == 'HIGH CARD':
        # Draws
        copy = sorted(hand.cards[:])

        # Test for flush draw
        maxsuit, qty = ev.dominant_suit(copy)

        if qty == 4:
            discard = ev.pop_suits(copy, maxsuit)

        # Test for open-ended straight draw(s)
        elif ev.get_allgaps(copy[0:4]) == 0:
            keep = copy[0:4]
        elif ev.get_allgaps(copy[1:5]) == 0:
            keep = copy[1:5]

        # Test for gutshot straight draw(s)
        elif ev.get_allgaps(copy[0:4]) == 1:
            keep = copy[0:4]
        elif ev.get_allgaps(copy[1:5]) == 1:
            keep = copy[1:5]

        # Draw to high cards
        elif card.RANKS[h[2][1]] > 9:
            highcards = h[0][1] + h[1][1] + h[2][1]
            discard = ev.pop_ranks(hand.cards, highcards)
        elif card.RANKS[h[1][1]] > 9:
            highcards = h[0][1] + h[1][1]
            discard = ev.pop_ranks(hand.cards, highcards)

        elif qty == 3:
            # Backdoor flush draw
            discard = ev.pop_suits(copy, maxsuit)

        # Draw to an Ace almost as a last resort
        elif h[1][1] == 'A':
            discard = ev.pop_ranks(hand.cards, 'A')

        # Backdoor straight draws are pretty desparate
        elif ev.get_allgaps(copy[0:3]) == 0:
            keep = copy[0:3]
        elif ev.get_allgaps(copy[1:4]) == 0:
            keep = copy[1:4]
        elif ev.get_allgaps(copy[2:5]) == 0:
            keep = copy[2:5]

        # 1-gap Backdoor straight draws are truly desparate!
        elif ev.get_allgaps(copy[0:3]) == 1:
            keep = copy[0:3]
        elif ev.get_allgaps(copy[1:4]) == 1:
            keep = copy[1:4]
        elif ev.get_allgaps(copy[2:5]) == 1:
            keep = copy[2:5]
        else:
            # Last ditch - just draw to the best 2???
            highcards = h[0][1] + h[1][1]
            discard = ev.pop_ranks(hand.cards, highcards)

        if len(discard) == 0:
            for c in hand.cards:
                if c not in keep:
                    discard.append(c)

    return discard


class Draw5Game(game.Game):
    def play(self):
        """ Defines the structure of a hand played in the game."""
        newround = game.Round(self)
        newround.cheat_check()

        # todo: Postblinds
        newround.post_blinds()

        # A simple 1-bet
        #  newround.ante_up()

        # Five card draw - deal 5 cards to each player
        newround.deal_cards(5)

        # Show table pre draw
        print(newround)
        print(self._table)

        # Pre-draw betting round
        newround.setup_betting()
        victor = newround.betting()

        if victor is None:
            #  newround.discard_phase()
            newround.muck.extend(discard_phase(self._table, newround.d))

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
        newround.muck_all_cards()
        # Remove broke players
        newround.remove_broke_players()

        # Move the table button
        self._table.move_button()

        # Advance round counter
        self.rounds += 1


def main():
    os.system('clear')
    print('FIVE CARD DRAW!')
    #  print('Initializing new game...\n')
    STAKES = blinds.limit['50/100']
    g = Draw5Game('FIVE CARD DRAW', STAKES, 6, 'LUNNA')

    playing = True

    while playing:
        print(g)
        g.play()
        choice = input('keep playing? > ')
        if choice.lower() == 'n' or choice == 0:
            playing = False

        os.system('clear')
    exit()


def test():
    print('Five Card Draw tests')
    print('')
    print('*'*80)
    print('Testing discard function')
    print('')
    r = pokerhands.dealhand(5)
    print('Random 5 cards: {}'.format(r))
    h = hand.Hand(r)
    print('Value: {:<15} Rank: {:<15}'.format(h.value, h.handrank))

    d = auto_discard(h)
    print('Discard: {}'.format(d))


if __name__ == "__main__":
    main()
    #  test()
