import card
import cardlist
import evaluator as ev
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
        discard = cardlist.strip_ranks(hand.cards, highcards)
    elif hand.handrank == 'TWO PAIR':
        # Keep the twp pair, discard 1.
        highcards = h[0][1] + h[1][1]

        discard = cardlist.strip_ranks(hand.cards, highcards)

    elif hand.handrank == 'HIGH CARD':
        # Draws
        copy = sorted(hand.cards[:])

        # Test for flush draw
        suit = ev.dominant_suit(copy)
        qty = cardlist.count_suit(copy, suit)

        if qty == 4:
            discard = cardlist.strip_suits(copy, suit)

        # Test for open-ended straight draw(s)
        elif cardlist.get_allgaps(copy[0:4]) == 0:
            keep = copy[0:4]
        elif cardlist.get_allgaps(copy[1:5]) == 0:
            keep = copy[1:5]

        # Test for gutshot straight draw(s)
        elif cardlist.get_allgaps(copy[0:4]) == 1:
            keep = copy[0:4]
        elif cardlist.get_allgaps(copy[1:5]) == 1:
            keep = copy[1:5]

        # Draw to high cards
        elif card.RANKS[h[2][1]] > 9:
            highcards = h[0][1] + h[1][1] + h[2][1]
            discard = cardlist.strip_ranks(hand.cards, highcards)
        elif card.RANKS[h[1][1]] > 9:
            highcards = h[0][1] + h[1][1]
            discard = cardlist.strip_ranks(hand.cards, highcards)

        elif qty == 3:
            # Backdoor flush draw
            discard = cardlist.strip_suits(copy, suit)

        # Draw to an Ace almost as a last resort
        elif h[1][1] == 'A':
            discard = cardlist.strip_ranks(hand.cards, 'A')

        # Backdoor straight draws are pretty desparate
        elif cardlist.get_allgaps(copy[0:3]) == 0:
            keep = copy[0:3]
        elif cardlist.get_allgaps(copy[1:4]) == 0:
            keep = copy[1:4]
        elif cardlist.get_allgaps(copy[2:5]) == 0:
            keep = copy[2:5]

        # 1-gap Backdoor straight draws are truly desparate!
        elif cardlist.get_allgaps(copy[0:3]) == 1:
            keep = copy[0:3]
        elif cardlist.get_allgaps(copy[1:4]) == 1:
            keep = copy[1:4]
        elif cardlist.get_allgaps(copy[2:5]) == 1:
            keep = copy[2:5]
        else:
            # Last ditch - just draw to the best 2???
            highcards = h[0][1] + h[1][1]
            discard = cardlist.strip_ranks(hand.cards, highcards)

        if len(discard) == 0:
            for c in hand.cards:
                if c not in keep:
                    discard.append(c)

    return discard
