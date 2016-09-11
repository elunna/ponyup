from __future__ import print_function
import card
import evaluator as ev


def made_hand_discards(hand, ranklist):
    """
    Determine the best cards to discard for a given made hand.
    hand is a Hand object.
    """
    PAT_HANDS = ['STRAIGHT', 'FLUSH', 'FULL HOUSE', 'STRAIGHT FLUSH', 'ROYAL FLUSH']
    DIS_RANKS = ['PAIR', 'TRIPS', 'QUADS']

    if hand.rank() in PAT_HANDS:
        return []  # Don't discard anything
    elif hand.rank() in DIS_RANKS:
        #  standard discard
        paircard = ranklist[0].rank
        return ev.strip_ranks(hand.cards, paircard)
    elif hand.rank() == 'TWO PAIR':
        # Keep the two pair, discard 1.
        paircard = ranklist[0].rank + ranklist[1].rank

        return ev.strip_ranks(hand.cards, paircard)


def auto_discard(hand, max_discards=5):
    """
    Calculates the best discard in a 5 card hand. Takes a maximum number of allowed discards. If
    the auto-pick for discards is larger than the max, we will pop out the lowest cards(thereby
    keeping the higher and more valuable cards) until we reach the allowable number.
    # hand is a Hand object
    """
    ranklist = ev.rank_list(hand.cards)
    if hand.rank() == 'HIGH CARD':
        # Process any available draws
        discards = draw_discards(sorted(hand.cards[:]), ranklist)
    else:
        discards = made_hand_discards(hand, ranklist)

    while len(discards) > max_discards:
        lowcard = min(discards)
        discards.remove(lowcard)

    return discards


def draw_discards(cards, ranklist):
    """
    Calculates the approprate card to discard for any draw-type hands.
    """
    suit = ev.dominant_suit(cards)
    suit_count = ev.count_suit(cards, suit)

    # Check 4 card draws first
    # Flush draws
    if suit_count == 4:
        return ev.strip_suits(cards, suit)

    # Test for open-ended straight draw(s)
    OESD = ev.chk_straight_draw(cards, 4, 0)
    if OESD is not None:
        return ev.extract_discards(cards, OESD)

    # Test for gutshot straight draw(s)
    GSSD = ev.chk_straight_draw(cards, 4, 1)
    if GSSD is not None:
        return ev.extract_discards(cards, GSSD)

    # Draw to high cards (J+)
    if card.RANKS[ranklist[2].rank] > 10:
        highcards = ''.join([ranklist[i].rank for i in range(3)])
        return ev.strip_ranks(cards, highcards)
    elif card.RANKS[ranklist[1].rank] > 10:
        highcards = ''.join([ranklist[i].rank for i in range(2)])
        return ev.strip_ranks(cards, highcards)

    # Draw to an Ace
    # We'll generally draw to an Ace over any backdoor draws.
    if ranklist[0].rank == 'A':
        return ev.strip_ranks(cards, 'A')

    if suit_count == 3:  # Backdoor flush draw
        return ev.strip_suits(cards, suit)

    # Backdoor straight draws are pretty desparate
    BDSD = ev.chk_straight_draw(cards, 3, 0)
    if BDSD is not None:
        return ev.extract_discards(cards, BDSD)

    # 1-gap Backdoor straight draws are truly desparate!
    BDSD = ev.chk_straight_draw(cards, 3, 1)
    if BDSD is not None:
        return ev.extract_discards(cards, BDSD)

    # Last ditch effort - just draw to the best 2.
    highcards = ''.join([ranklist[i].rank for i in range(2)])
    return ev.strip_ranks(cards, highcards)


def discard_phase(_round):
    """
    Goes through a table and offers all players with cards the option to discard.
    Returns a list of all the discards (ie:"muck" cards)
    """
    _round.out('DISCARD PHASE:', decorate=True)
    cardholders = _round._table.get_players(hascards=True)

    for s in cardholders:
        max_discards = (5 if len(_round.d) >= 5 else len(_round.d))
        if max_discards == 0:
            _round.out('Deck has been depleted!')
            break

        if s.player.is_human():
            discards = human_discard(s.hand, max_discards)
        else:
            discards = auto_discard(s.hand, max_discards)

        if discards:
            _round.out('{} discards {}'.format(str(s), discards))
        else:
            _round.out('{} stands pat.'.format(str(s)))

        # Discard
        for c in discards:
            _round.discard(s, c)

        # Redraw
        drawpile = redraw(s, _round.d)
        _round.out('{} draws {}'.format(str(s.player), drawpile))


def redraw(seat, deck, handsize=5):
    """
    Player draws cards back up to the normal handsize.
    """
    drawpile = []
    while len(seat.hand) < handsize:
        draw = deck.deal()

        if seat.player.is_human():  # Unhide our cards so we can see them.
            draw.hidden = False

        seat.hand.add(draw)
        drawpile.append(draw)

    return drawpile


def human_discard(hand, max_discards=5):
    """
    Offers the human player a menu of discard options and returns the list of chosen discards.
    """
    print(discard_menu(hand))
    while True:
        helpme = ['?', 'h', 'help']
        user_str = input(':> ')
        if user_str in helpme:
            print('')
            print('Enter the cards you want to discard:')
            print('Example: "1" discards card 1, "12" discards cards 1 and 2, etc.')
            continue

        # Note: x is checking if there is a str x in valid_picks.
        picks = [int(x) for x in set(user_str) if x in valid_picks(hand)]

        if len(picks) > max_discards:
            print('Sorry, the deck is low -- you can only pick up to {} cards.'.format(
                max_discards))
            continue

        return get_discards(hand, picks)


def get_discards(hand, picks):
    if len(hand) == 0:
        raise ValueError('Hand is empty! Cannot pick any discards!')

    return [hand.cards[n] for n in picks]


def valid_picks(hand):
    """
    Create a list of all the indexes(in string format) of cards in the given hand.
    List starts from 0.
    """
    return list(map(str, range(len(hand))))


def discard_menu(hand):
    indices = ''.join(['{:<3}'.format(n) for n in valid_picks(hand)])

    txt = indices + '\n'
    #  txt += ' '.join([(c) for c in hand.peek()])
    txt += hand.peek()
    txt += '\n'
    return txt
