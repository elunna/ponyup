import unittest
from ponyup import blinds
from ponyup import card
from ponyup import factory
from ponyup import poker
from ponyup import tools


class TestPoker(unittest.TestCase):
    """
    Setup a session and round, with a table filled with 6 players.
    """
    def setUp(self, lvl=1, players=6):
        # Make a 6 player table
        self.g = factory.session_factory(seats=players, game="FIVE CARD DRAW", level=lvl)
        self.r = poker.Round(self.g)

    def setUp_stud(self, lvl=1, players=6):
        self.g = factory.session_factory(seats=players, game="FIVE CARD STUD", level=lvl)
        self.r = poker.Round(self.g)

    def givehand(self, seat, hand):
        self.r.table.seats[seat].hand.cards = tools.make(hand)

    """
    Tests for __init__()
    """
    # Round __init__(): Pot = 0

    """
    Tests for __str__()
    """
    # None yet.

    """
    Tests for log
    """
    # Make into a decorator?

    """
    Tests for deal_cards(qty, faceup=False)
    """
    # 6 players, deal 1 - should be 6 cardholders
    def test_dealcards_deal1_6cardholders(self):
        self.r.table.move_button()
        self.r.table.set_blinds()
        self.r.deal_cards(1)
        expected = 6
        result = len(self.r.table.get_players(hascards=True))
        self.assertEqual(expected, result)

    # 6 players, deal 1 - decksize == 48
    def test_dealcards_deal1_decksize48(self):
        self.r.deal_cards(1)
        expected = 46
        result = len(self.r.d)
        self.assertEqual(expected, result)

    # 6 players, deal 1 (no keyword arg) - cards are hidden
    def test_dealcards_deal1_cardsarehidden(self):
        self.r.deal_cards(1)
        for s in self.r.table:
            expected = 0
            result = len(s.hand.get_upcards())
            self.assertEqual(expected, result)

    # 6 players, deal 1 (faceup=True) - cards are faceup
    def test_dealcards_deal1_faceup_cardsarenothidden(self):
        self.r.deal_cards(1, faceup=True)
        for s in self.r.table:
            self.assertFalse(s.hand.cards[0].hidden)

    # 5 players have cards, deal only to those that still have cards
    def test_dealcards_deal6deal5toands_deckis41cards(self):
        self.r.deal_cards(1)  # Deal 6 cards
        self.r.table.seats[0].fold()
        self.r.deal_cards(1, handreq=True)  # Deal 5 cards
        self.assertEqual(len(self.r.d), 41)

    """
    Tests show_cards()
    """
    # Deal facedown cards to 2 players, should be able to see CPU cards

    """
    Tests for sortcards()
    """
    # deal highcards1():
    #  h = [('A', 'd'), ('4', 's'), ('Q', 's'), ('7', 's'), ('K', 'h')]
    def test_sortcards_humandealt_sorted(self):
        h = tools.make('highcards')
        self.r.table.seats[0].hand.cards = h[:]
        expected = sorted(h)
        self.r.sortcards()
        result = self.r.table.seats[0].hand.cards
        self.assertEqual(expected, result)

    """
    Tests for burn()
    """
    # Burn 1 card, deck is 1 less
    def test_burn_decksize_decreased1(self):
        decksize = len(self.r.d)
        self.r.burn()
        expected = 1
        result = decksize - len(self.r.d)
        self.assertEqual(expected, result)

    # Burn 1 card, muck is 1 more
    def test_burn_mucksize_increased1(self):
        mucksize = len(self.r.muck)
        self.r.burn()
        expected = 1
        result = len(self.r.muck) - mucksize
        self.assertEqual(expected, result)

    # Burn, empty deck, nothing happens

    """
    Tests for muck_all_cards()
    """
    # 6 players, deal 1 - no cardholders after running
    def test_muckallcards_cardsmucked_nocardholders(self):
        self.r.table.move_button()
        self.r.table.set_blinds()
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 0
        result = len(self.r.table.get_players(hascards=True))
        self.assertEqual(expected, result)

    # 6 players, deal 1 - verify_muck is True after running
    def test_muckallcards_cardsmucked_verifymuckreturnsTrue(self):
        self.r.table.move_button()
        self.r.table.set_blinds()
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = True
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    # 6 players, deal 1 - decksize == 0 after running
    def test_muckallcards_cardsmucked_decksize0(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 0
        result = len(self.r.d)
        self.assertEqual(expected, result)

    # 6 players, deal 1 - muck size == 52 after running
    def test_muckallcards_cardsmucked_mucksize52(self):
        self.r.deal_cards(1)
        self.r.muck_all_cards()
        expected = 52
        result = len(self.r.muck)
        self.assertEqual(expected, result)

    """
    Tests for post_antes()
    """
    # 6 players ante 1. Pot == 6.
    def test_postantes_6players_potequals60(self):
        self.r.blinds = blinds.Blinds(level=2, antes=True)
        self.r.post_antes()
        expected = 6
        result = self.r.pot
        self.assertEqual(expected, result)

    # Initial stacks=1000. Ante=1. After ante are 999.
    def test_postantes_6players_stacksequal999(self):
        self.r.blinds = blinds.Blinds(level=2, antes=True)
        self.r.post_antes()
        expected = 999
        for s in self.r.table:
            result = s.stack
            self.assertEqual(expected, result)

    """
    Tests for post_blinds()
    """
    # If the button(and blinds haven't been set, raise an exception.)
    def test_postblinds_btnnotset_raiseException(self):
        self.r.table.TOKENS['D'] = -1
        self.assertEqual(self.r.table.TOKENS['D'], -1, 'Button should be -1!')
        self.assertRaises(Exception, self.r.post_blinds)

    # 2 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_2players_pot3(self):
        for i in [1, 2, 4, 5]:
            self.r.table.pop(i)
        self.r.table.TOKENS['D'] = -1
        self.r.table.move_button()  # verify the button is 0
        self.r.table.set_blinds()
        self.assertEqual(self.r.table.TOKENS['D'], 0)
        self.r.post_blinds()
        self.assertEqual(self.r.table.seats[0].stack, 999)
        self.assertEqual(self.r.table.seats[3].stack, 998)
        self.assertEqual(self.r.pot, 3)

    # 3 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_3players_pot3(self):
        for i in [1, 3, 5]:
            self.r.table.pop(i)

        self.r.table.TOKENS['D'] = -1
        self.r.table.move_button()  # verify the button is 0
        self.r.table.set_blinds()
        self.assertEqual(self.r.table.TOKENS['D'], 0)
        self.r.post_blinds()
        self.assertEqual(self.r.table.seats[2].stack, 999)
        self.assertEqual(self.r.table.seats[4].stack, 998)
        self.assertEqual(self.r.pot, 3)

    # 6 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_6players_pot3(self):
        self.r.table.TOKENS['D'] = -1
        self.r.table.move_button()
        self.r.table.set_blinds()
        self.assertEqual(self.r.table.TOKENS['D'], 0)  # verify the button is 0
        self.r.post_blinds()
        self.assertEqual(self.r.table.seats[1].stack, 999)
        self.assertEqual(self.r.table.seats[2].stack, 998)
        self.assertEqual(self.r.pot, 3)

    # 6 players(spaced out). SB=1, BB=2, startingstacks=1000
    def test_postblinds_6players_returnsString(self):
        self.setUp(lvl=1)
        self.r.table.TOKENS['D'] = -1
        self.r.table.move_button()
        self.r.table.set_blinds()
        self.assertEqual(self.r.table.TOKENS['D'], 0)  # verify the button is 0
        expected = 'bob1 posts $1\nbob2 posts $2'
        result = self.r.post_blinds()
        self.assertEqual(expected, result)

    """
    Tests for post_bringin():
    """
    # Initial stacks=1000.
    # Seat 0
    def test_postbringin_seat5_has2chipsless(self):
        self.setUp_stud()
        tools.deal_stud5(self.r.table, matchingranks=0)
        self.r.table.set_bringin()
        BI = self.r.table.TOKENS['BI']
        seat = self.r.table.seats[BI]
        stack = seat.stack
        self.r.post_bringin()
        expected = 1
        result = stack - seat.stack
        self.assertEqual(expected, result)

    def test_postbringin_seat5_returnsString(self):
        self.setUp_stud()
        tools.deal_stud5(self.r.table, matchingranks=0)
        expected = 'bob5 brings it in for $1'
        self.r.table.set_bringin()
        result = self.r.post_bringin()
        self.assertEqual(expected, result)

    """
    Tests for next_street()
    """
    def test_nextstreet_street0_streetIs1(self):
        self.r.next_street()
        expected = 1
        result = self.r.street
        self.assertEqual(expected, result)

    def test_nextstreet_draw5_street2_raisesException(self):
        self.r.next_street()
        self.r.next_street()
        self.assertRaises(Exception, self.r.next_street)

    """
    Tests for get_street()
    """

    """
    Tests for one_left()
    """
    def test_oneleft_allhavecards_returnsNone(self):
        self.setUp(players=2)
        self.r.deal_cards(1)
        expected = None
        result = self.r.one_left()
        self.assertEqual(expected, result)

    def test_oneleft_1withcards_returnsvictor(self):
        self.setUp(players=2)
        self.r.deal_cards(1)
        self.r.table.pop(0)
        victor = self.r.table.seats[1]
        expected = victor
        result = self.r.one_left()
        self.assertEqual(expected, result)

    """
    Tests for betting_round()
    """

    """
    Tests for betting_over()
    """
    def test_bettingover_2hands1broke_returnsTrue(self):
        self.setUp(players=2)
        self.r.deal_cards(1)
        self.r.table.seats[0].stack = 0
        expected = True
        result = self.r.betting_over()
        self.assertEqual(expected, result)

    def test_bettingover_3hands1broke_returnsFalse(self):
        self.setUp(players=3)
        self.r.deal_cards(1)
        self.r.table.seats[0].stack = 0
        expected = False
        result = self.r.betting_over()
        self.assertEqual(expected, result)

    """
    Tests for found_winner()
    """

    """
    Tests for showdown()
    """

    """
    Tests for cleanup()
    """
    # After cleanup, there should be no broke players.
    """
    def test_cleanup(self):
        self.r.muck_all_cards()
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)
    """

    # After cleanup, no players should have cards
    def test_cleanup_noplayershavecards(self):
        self.r.muck_all_cards()
        expected = []
        result = self.r.table.get_players(hascards=True)
        self.assertEqual(expected, result)

    # After cleanup, there should be no cards in the deck
    def test_cleanup_deckisempty(self):
        self.r.muck_all_cards()
        expected = True
        result = self.r.d.is_empty()
        self.assertEqual(expected, result)

    # After cleanup, the muck size should equal the starting deck size
    def test_cleanup_muck_deck_sizesequal(self):
        self.r.muck_all_cards()
        expected = self.r.DECKSIZE
        result = len(self.r.muck)
        self.assertEqual(expected, result)

    """
    Tests for check_integrity_pre(self):
    """

    """
    Tests for check_integrity_post(self):
    """
    # All cards mucked, but 1 card in deck, returns False
    def test_checkintegritypost_1cardindeck_returnsFalse(self):
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r.d.cards.append(c)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    # All cards mucked, but 1 player w cards, returns False
    def test_checkintegritypost_1playerwithcards_returnsFalse(self):
        self.r.table.move_button()
        self.r.table.set_blinds()
        self.r.muck_all_cards()
        c = card.Card('A', 's')
        self.r.table.seats[0].hand.add(c)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    # All cards mucked, but card in muck deleted, returns False
    def test_checkintegritypost_1poppedfrommuck_returnsFalse(self):
        self.r.muck_all_cards()
        self.r.muck.pop(0)
        expected = False
        result = self.r.check_integrity_post()
        self.assertEqual(expected, result)

    """
    Tests for highhand(table)
    """
    # Throw in an empty seat for testing.
    # Throw in a player without cards for testing.

    # Stud5:
    def test_highhand_3cards_pairAces_return0(self):
        self.setUp(players=3)
        self.givehand(0, '2AA_v1')
        self.givehand(1, '2KK')
        self.givehand(2, '2QQ')
        self.r.table.set_bringin()
        expected = 0
        result = self.r.highhand()
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_4cards_AceHigh_return0(self):
        self.setUp(players=4)
        self.givehand(0, 'QKA_v1')
        self.givehand(1, 'JTQ')
        self.givehand(2, '89J')
        self.givehand(3, '567')
        self.r.table.set_bringin()
        expected = 0
        result = self.r.highhand()
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_3cards_2tied_return02(self):
        self.setUp(players=3)
        self.givehand(0, '2AA_v1')
        self.givehand(1, '2KK')
        self.givehand(2, '2AA_v2')  # Ad is bringin; dealt first
        self.r.table.set_bringin()
        expected = 2
        result = self.r.highhand()
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_4cards_2tied_return02(self):
        self.setUp(players=4)
        self.givehand(0, 'QKA_v1')  # Dealt first on 4th street
        self.givehand(1, 'JTQ')
        self.givehand(2, 'QKA_v2')
        self.givehand(3, '567')     # Bringin
        self.r.table.set_bringin()
        expected = 0
        result = self.r.highhand()
        self.assertEqual(expected, result)

    # Stud5:
    def test_highhand_3cards_3tied_return023(self):
        self.setUp(players=6)
        self.givehand(0, '3AK_v1')  # Dealt first on 4th street
        self.givehand(1, '3AK_v2')
        self.givehand(2, '3AK_v3')
        self.givehand(3, '345')
        self.givehand(4, '234')     # Bringin
        self.givehand(5, '245')
        self.r.table.set_bringin()
        expected = 0
        result = self.r.highhand()
        self.assertEqual(expected, result)
