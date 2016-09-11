import unittest
import deck
import discard
import hand
import pokerhands
import seat


class TestDiscard(unittest.TestCase):
    def setUp(self, handsize=1):
        self.d = deck.Deck()
        self.s = seat.Seat(0)

        for i in range(handsize):
            self.s.hand.add(self.d.deal())

    """
    Tests for auto_discard(hand):
    """
    # Royal flush - no discards
    def test_autodiscard_royalflush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.make('royalflush'))
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Straight flush - no discards
    def test_autodiscard_straightflush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.make('straightflush_high'))
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Full house - no discards
    def test_autodiscard_fullhouse_returnsEmptyList(self):
        h = hand.Hand(pokerhands.make('fullhouse_high'))
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Flush - no discards
    def test_autodiscard_flush_returnsEmptyList(self):
        h = hand.Hand(pokerhands.make('flush_low'))
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Straight - no discards
    def test_autodiscard_straight_returnsEmptyList(self):
        h = hand.Hand(pokerhands.make('straight_mid'))
        h.unhide()
        expected = []
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Quads - discard the non quad card
    def test_autodiscard_quads_returns1card(self):
        # [('A', 's'), ('A', 'd'), ('A', 'h'), ('A', 'c'), ('K', 'c')]
        h = hand.Hand(pokerhands.make('quads_high'))
        h.unhide()
        expected = ['Kc']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        #  result = sorted([repr(c) for c in draw5.auto_discard(h)])
        self.assertEqual(expected, result)

    # Trips - discard the non-trip cards
    def test_autodiscard_trips_returns2cards(self):
        # [('A', 's'), ('K', 'h'), ('A', 'h'), ('A', 'd'), ('Q', 'c')]
        h = hand.Hand(pokerhands.make('trips_high'))
        h.unhide()
        expected = ['Qc', 'Kh']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Pair - Discard the non-pair cards
    def test_autodiscard_pair_returns3cards(self):
        # [('K', 's'), ('Q', 'h'), ('A', 's'), ('A', 'd'), ('J', 'c')]
        h = hand.Hand(pokerhands.make('pair_high'))
        h.unhide()
        expected = ['Jc', 'Qh', 'Ks']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Two-Pair - Discard the non-pair card
    def test_autodiscard_2pair_returns1card(self):
        # [('A', 's'), ('A', 'h'), ('K', 's'), ('K', 'd'), ('Q', 'c')]
        h = hand.Hand(pokerhands.make('twopair_high'))
        h.unhide()
        expected = ['Qc']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # OESFD - Discard the non-flush card
    def test_autodiscard_OESFD_returns1card(self):
        # [('J', 's'), ('T', 's'), ('8', 's'), ('2', 'd'), ('9', 's')]
        h = hand.Hand(pokerhands.make('OESFD'))
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # GSSFD - Discard the non-flush card
    def test_autodiscard_GSSFD_returns1card(self):
        # [('J', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
        h = hand.Hand(pokerhands.make('GSSFD'))
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Flush draw - Discard the non-flush card
    def test_autodiscard_flushdraw_returns1card(self):
        # [('A', 's'), ('T', 's'), ('7', 's'), ('2', 'd'), ('9', 's')]
        h = hand.Hand(pokerhands.make('flushdrawA'))
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # OESD - Discard the non-straight card
    def test_autodiscard_OESD_returns1card(self):
        # [('J', 'h'), ('T', 's'), ('8', 'c'), ('2', 'd'), ('9', 's')]
        h = hand.Hand(pokerhands.make('OESD'))
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # GSSD - Discard the non-straightcard
    def test_autodiscard_GSSD_returns(self):
        # [('J', 'h'), ('T', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
        h = hand.Hand(pokerhands.make('GSSD'))
        h.unhide()
        expected = ['2d']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Wheel draw - Discard the high card
    def test_autodiscard_wheel_returns(self):
        # [('3', 'h'), ('4', 's'), ('A', 's'), ('2', 'd'), ('K', 'h')]
        h = hand.Hand(pokerhands.make('wheeldraw'))
        h.unhide()
        expected = ['Kh']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # BDFD(low cards) - Discard the non-flush cards
    def test_autodiscard_BDFD1returns2cards(self):
        # [('2', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('K', 'h')]
        h = hand.Hand(pokerhands.make('BDFD1'))
        h.unhide()
        expected = ['2d', 'Kh']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # BDFD(with 2 high cards) - Discard the low cards
    def test_autodiscard_BDFD2returns3cards(self):
        # [('A', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('K', 'h')]
        h = hand.Hand(pokerhands.make('BDFD2'))
        h.unhide()
        expected = ['4s', '5s', '7s']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # 3 High cards - Discard the 2 low cards
    def test_autodiscard_highcards_returns2cards(self):
        # [('A', 'd'), ('4', 's'), ('Q', 's'), ('7', 's'), ('K', 'h')]
        h = hand.Hand(pokerhands.make('highcards'))
        h.unhide()
        expected = ['4s', '7s']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Ace high - Discard the non-pair card
    def test_autodiscard_acehigh_returns4cards(self):
        # [('A', 'd'), ('4', 's'), ('5', 's'), ('7', 's'), ('9', 'h')]
        h = hand.Hand(pokerhands.make('acehigh'))
        h.unhide()
        expected = ['4s', '5s', '7s', '9h']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # 0 gap BDSD - Discard the non-connected cards
    def test_autodiscard_BDSD_returns2cards(self):
        # [('2', 'd'), ('7', 's'), ('8', 's'), ('9', 'd'), ('K', 'h')]
        h = hand.Hand(pokerhands.make('BDSD1'))
        h.unhide()
        expected = ['2d', 'Kh']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # 1 gap BDSD - Discard the non-connected cards
    def test_autodiscard_BDSD2_returns2cards(self):
        # [('2', 'd'), ('7', 's'), ('8', 's'), ('9', 'd'), ('K', 'h')]
        h = hand.Hand(pokerhands.make('BDSD2'))
        h.unhide()
        expected = ['2d', 'Kh']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    # Medium cards/junk - Discard the 3 low cards
    def test_autodiscard_junk_returns(self):
        #  [('2', 'd'), ('3', 's'), ('6', 's'), ('8', 'd'), ('T', 'h')]
        h = hand.Hand(pokerhands.make('junk'))
        h.unhide()
        expected = ['2d', '3s', '6s']
        result = [repr(c) for c in sorted(discard.auto_discard(h))]
        self.assertEqual(expected, result)

    """
    Tests for get_discards(hand, picks):
    """
    # Empty hand, raise exception
    def test_getdiscards_emptyhand_raisesException(self):
        h = hand.Hand()
        picks = [0, 4]
        self.assertRaises(ValueError, discard.get_discards, h, picks)

    # Empty picks, return empty list
    def test_getdiscards_nopicks_returnsEmptylist(self):
        h = hand.Hand(pokerhands.convert_to_cards(['As', 'Ks', 'Qs']))
        picks = []
        expected = []
        result = discard.get_discards(h, picks)
        self.assertEqual(expected, result)

    # picks 0, gets card at index 0
    def test_getdiscards_pick0_returnsCard0(self):
        cards = pokerhands.convert_to_cards(['As', 'Ks', 'Qs'])
        h = hand.Hand(cards)
        picks = [0]
        expected = [cards[0]]
        result = discard.get_discards(h, picks)
        self.assertEqual(expected, result)

    # picks 0 and 1, gets cards at index 0 and 1
    def test_getdiscards_pick01_returnsCard0and1(self):
        cards = pokerhands.convert_to_cards(['As', 'Ks', 'Qs'])
        h = hand.Hand(cards)
        picks = [0, 1]
        expected = [cards[0], cards[1]]
        result = discard.get_discards(h, picks)
        self.assertEqual(expected, result)

    """
    Tests for valid_picks(hand)
    """
    # Empty hand, returns empty list
    def test_validpicks_handsize0_returnEmptylist(self):
        h = hand.Hand()
        expected = []
        result = discard.valid_picks(h)
        self.assertEqual(expected, result)

    # 1 card in hand, returns [0]
    def test_validpicks_handsize1_returnInts0(self):
        cards = pokerhands.convert_to_cards(['As'])
        h = hand.Hand(cards)
        expected = [0]
        result = discard.valid_picks(h)
        self.assertEqual(expected, result)

    # 3 cards in hand, returns [0, 1, 2]
    def test_validpicks_handsize3_returnInts012(self):
        cards = pokerhands.convert_to_cards(['As', 'Ks', 'Qs'])
        h = hand.Hand(cards)
        expected = [0, 1, 2]
        result = discard.valid_picks(h)
        self.assertEqual(expected, result)

    """
    Tests for discard_menu(hand):
    """
    # 1 card in hand, shows index and card
    def test_discardmenu_1card_returnsMenu(self):
        cards = pokerhands.convert_to_cards(['As'])
        h = hand.Hand(cards)
        expected = '0  \nAs\n'
        result = discard.discard_menu(h)
        self.assertEqual(expected, result)

    # 1 card in hand, shows index and card
    def test_discardmenu_2cards_returnsMenu(self):
        cards = pokerhands.convert_to_cards(['As', 'Ks'])
        h = hand.Hand(cards)
        expected = '0  1  \nAs Ks\n'
        result = discard.discard_menu(h)
        self.assertEqual(expected, result)

    """
    Tests for redraw(players, handsize=5):
    """

    # CPU, 4 cards, draws 1 card.
    def test_redraw_4cardhand_draw1(self):
        self.setUp(handsize=4)
        expected = 1
        result = len(discard.redraw(self.s, self.d))
        self.assertEqual(expected, result)

    # CPU, 3 cards, draws 2 cards.
    # CPU, 4 cards, draws 1 hidden card.

    # human, 4 cards, draws 1 card.
    # human, 4 cards, draws 1 faceup card.

    # CPU, 4 cards, handsize=4, draws 0 cards.
