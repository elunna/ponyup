from __future__ import print_function
import card
import cardlist
import evaluator as ev
import poker

DEALT = 5


class Draw5Session(poker.Session):
    def play(self):
        """ Play a round of Five Card Draw."""
        _round = poker.Round(self)

        if len(self._table.get_cardholders()) > 0:
            raise Exception('One or more players have cards before the deal!')

        _round.post_blinds()
        _round.deal_cards(DEALT)
        _round.sortcards()

        print(self._table)      # Show table pre draw

        # Pre-draw betting
        _round.setup_betting()
        victor = _round.betting_round()

        print(_round)           # Display pot

        if victor is None:
            # Discard phase
            discards = discard_phase(self._table, _round.d)
            _round.muck.extend(discards)
            _round.sortcards()

            print(self._table)  # Show table post draw

            # Post-draw betting round
            _round.setup_betting()
            victor = _round.betting_round()

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
    PAT_HANDS = ['STRAIGHT', 'FLUSH', 'FULL HOUSE', 'STRAIGHT FLUSH', 'ROYAL FLUSH']
    DIS_RANKS = ['PAIR', 'TRIPS', 'QUADS']

    ranklist = cardlist.rank_list(hand.cards)

    if hand.handrank in PAT_HANDS:
        return []  # Don't discard anything
    elif hand.handrank in DIS_RANKS:
        #  standard discard
        highcards = ranklist[0].rank
        return cardlist.strip_ranks(hand.cards, highcards)
    elif hand.handrank == 'TWO PAIR':
        # Keep the two pair, discard 1.
        highcards = ranklist[0].rank + ranklist[1].rank

        return cardlist.strip_ranks(hand.cards, highcards)

    # Process any available draws
    return draw_discards(sorted(cardlist.cards[:]), ranklist)


def draw_discards(cards, ranklist):
    suit = ev.dominant_suit(cards)
    suit_count = cardlist.count_suit(cards, suit)

    if suit_count == 4:
        return cardlist.strip_suits(cards, suit)

    # Test for open-ended straight draw(s)
    OESD = check_draw(cards, 4, 0)
    if OESD is not None:
        return extract_discards(OESD)

    # Test for gutshot straight draw(s)
    GSSD = check_draw(cards, 4, 1)
    if GSSD is not None:
        return extract_discards(GSSD)

    # Draw to high cards
    if card.RANKS[ranklist[2].rank] > 9:
        highcards = ''.join([ranklist[i].rank for i in range(3)])
        return cardlist.strip_ranks(cards, highcards)
    elif card.RANKS[ranklist[1].rank] > 9:
        highcards = ''.join([ranklist[i].rank for i in range(2)])
        return cardlist.strip_ranks(cards, highcards)

    if suit_count == 3:  # Backdoor flush draw
        return cardlist.strip_suits(cards, suit)

    # Draw to an Ace almost as a last resort
    elif ranklist[1].rank == 'A':
        return cardlist.strip_ranks(cards, 'A')

    # Backdoor straight draws are pretty desparate
    BDSD = check_draw(cards, 3, 0)
    if BDSD is not None:
        return extract_discards(OESD)

    # 1-gap Backdoor straight draws are truly desparate!
    BDSD = check_draw(cards, 3, 1)
    if BDSD is not None:
        return extract_discards(OESD)

    # Last ditch - just draw to the best 2???
    highcards = ''.join([ranklist[i].rank for i in range(2)])
    return cardlist.strip_ranks(cards, highcards)


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

            p.add_card(draw)
        print('')
    print('')

    return muckpile


def human_discard(hand):
    print('*'*40)
    print(' '*35 + '1  2  3  4  5')
    print(' '*35, end='')
    for c in hand.cards:
        print('{} '.format(str(c)), end='')
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


def is_integer(num):
    """ Determines if the variable is an integer"""
    try:
        int(num)
        return True
    except ValueError:
        return False


def check_draw(cards, qty, gap):
    # Assume cards are sorted
    for i in range((len(cards)-qty)+1):
        if cardlist.get_allgaps(card[i:qty+i]) == 0:
            return card[i:qty+i]
    else:
        return None


def extract_discards(cards, keep):
    return [c for c in cards if c not in keep]
