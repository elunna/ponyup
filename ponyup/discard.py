"""
  " Manages the discarding of cards in a poker hand. This module specifically
  " addresses the optimal discarding strategy for computer opponents.
  """
from __future__ import print_function
from ponyup import card
from ponyup import evaluator as ev
from ponyup import logger

_logger = logger.get_logger(__name__)


class Discard(object):
    """ Goes through a table and offers all players with cards the option to
        discard.  Returns a list of all the discards (ie:"muck" cards)
    """
    def __init__(self, _round):
        self.round = _round
        self.players = _round.table.get_players(hascards=True)
        self.handsize = 5
        self.done = False

        if len(self.players) == 0:
            raise Exception('No players available to discard!')

        _logger.debug('New Discard object created.')

    def __getattr__(self, name):
        try:
            return getattr(self.round, name)
        except AttributeError:
            raise AttributeError("Child' object has no attribute {}".format(name))

    def genny(self):
        # Generator
        if self.done:
            raise Exception('Already executed discard for this round!')
        for p in self.players:
            yield p

        self.done = True
        raise StopIteration()

    def max_discards(self):
        maxd = (self.handsize if len(self.d) >= self.handsize else len(self.d))
        _logger.debug('Maximum number of discards: {}'.format(maxd))
        return maxd

    def cpu_discard(self, seat):
        _logger.debug('CPU discard for: {} '.format(seat))
        if seat.player.is_human():
            raise Exception('Human player is trying to access cpu_discard.')

        cpu_hand = seat.hand
        return auto_discard(cpu_hand, self.max_discards())

    def discard(self, seat, discards):
        _logger.debug('Discarding {} for {} '.format(discards, seat))

        for c in discards:
            # Muck the discard
            self.muck.append(seat.hand.discard(c))

    def redraw(self, s):
        """ Player draws cards back up to the normal handsize. """
        drawpile = []
        while len(s.hand) < self.handsize:
            draw = self.d.deal()
            s.hand.add(draw)
            drawpile.append(draw)
        return drawpile


def discard_phase(_round):
    """ Goes through a table and offers all players with cards the option to
        discard. Returns a list of all the discards (ie:"muck" cards)
    """
    title = 'Discard Phase:'
    _logger.info(_round.decorate(title))
    dis = Discard(_round)

    for s in dis.genny():
        # Check if cards are left in deck
        if dis.max_discards == 0:
            _logger.info('Deck has been depleted!')
            break

        if s.player.is_human():
            discards = human_discard(s, dis.max_discards())
        else:
            discards = dis.cpu_discard(s)

        dis.discard(s, discards)
        d_txt = dis.discard_text(s, discards)
        dis.redraw(s)
        print(d_txt)


def auto_discard(hand, max_discards=5):
    """ Calculates the best discard in a 5 card hand. Takes a maximum number of
        allowed discards. If the auto-pick for discards is larger than the max,
        we will pop out the lowest cards(thereby keeping the higher and more
        valuable cards) until we reach the allowable number.
        hand is a Hand object
    """
    _logger.debug('auto_discard for {}.'.format(hand))

    ranklist = ev.rank_list(hand.cards)

    if hand.rank() == 'HIGH CARD':
        _logger.debug('Hand is a draw-type hand, finding best discard.')
        discards = draw_discards(sorted(hand.cards[:]), ranklist)
    else:
        _logger.debug('Hand is a made-hand, finding best discard.')
        discards = made_hand_discards(hand, ranklist)

    while len(discards) > max_discards:
        _logger.debug('The quantity of discards is greater than the max allowed discards.')
        lowcard = min(discards)
        _logger.debug('Pruning 1 card from the discards.')
        discards.remove(lowcard)

    _logger.debug('Returning these discards: {}.'.format(discards))
    return discards


def made_hand_discards(hand, ranklist):
    """ Determine the best cards to discard for a given made hand.
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


def draw_discards(cards, ranklist):
    """ Calculates the approprate card to discard for any draw-type hands. """

    if len(cards) != 5:
        raise ValueError('Card list needs to be 5 cards for a valid discard.')
    suit = ev.dominant_suit(cards)
    suit_count = ev.count_suit(cards, suit)

    # Check 4 card draws first
    # Flush draws
    if suit_count == 4:
        return ev.strip_suits(cards, suit)

    # Test for open-ended straight draw(s)
    OESD = ev.chk_straight_draw(cards, 4, 0)
    if OESD is not None:
        return extract_discards(cards, OESD)

    # Test for gutshot straight draw(s)
    GSSD = ev.chk_straight_draw(cards, 4, 1)
    if GSSD is not None:
        return extract_discards(cards, GSSD)

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
        return extract_discards(cards, BDSD)

    # 1-gap Backdoor straight draws are truly desparate!
    BDSD = ev.chk_straight_draw(cards, 3, 1)
    if BDSD is not None:
        return extract_discards(cards, BDSD)

    # Last ditch effort - just draw to the best 2.
    highcards = ''.join([ranklist[i].rank for i in range(2)])
    return ev.strip_ranks(cards, highcards)


def discard_menu(hand):
    indices = ''.join(['{:<3}'.format(n) for n in valid_picks(hand)])
    txt = indices + '\n'
    txt += hand.peek() + '\n'
    return txt


def valid_picks(hand):
    """ Create a list of all the indexes(in string format) of cards in the given
        hand. List starts from 0.
    """
    return list(map(str, range(1, len(hand) + 1)))


def get_discards(hand, picks):
    if len(hand) == 0:
        raise ValueError('Hand is empty! Cannot pick any discards!')
    for n in picks:
        if n < 1 or n > len(hand):
            raise ValueError('An index is out of bounds!')
    return [hand.cards[n - 1] for n in picks]


def human_discard(seat, max_discards=5):
    """ Offers the human player a menu of discard options and returns the list
        of chosen discards.
    """
    hand = seat.hand
    print(discard_menu(hand))
    while True:
        helpme = ['?', 'h', 'help']
        c = input(':> ')
        if c in helpme:
            print('')
            print('Enter the cards you want to discard:')
            print('Example: "1" discards card 1, "12" discards cards 1 and 2, etc.')
            continue

        # Note: x is checking if there is a str x in valid_picks.
        picks = [int(x) for x in set(c) if x in valid_picks(hand)]

        if len(picks) > max_discards:
            print('Sorry, the deck is low -- you can only pick up to {} cards.'.format(
                max_discards))
            continue

        return get_discards(hand, picks)


def extract_discards(cards, keep):
    """ Returns the cards we should discard from a group of cards.  """
    if len(cards) == 0 or cards is None:
        raise ValueError('Card list needs to contain some cards!')
    for c in keep:
        if c not in cards:
            raise ValueError('The keep list has a card not in the original card list!')

    return [c for c in cards if c not in keep]


def discard_text(seat, discards):
    if discards:
        d_txt = '{} discards {} cards'.format(seat.player, len(discards))
    else:
        d_txt = '{} stands pat.'.format(seat.player)

    _logger.info(d_txt)
    return d_txt
