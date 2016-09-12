import unittest


class TestHandAnalysis(unittest.TestCase):
    #  def __init__(self):
        #  super(TestCombos, self).__init__()
        #  d = deck.Deck()
        #  self.combosof5 = combos.get_combolist(d.cards, 5)
        #  self.type_count = combos.typecount_dict(combosof5)

    """
    Tests for typecount_dict(handlist)
    """
    # Since this dict is VERY LARGE, We will call all the tests from this constructor method.
    # DISABLED TEMPARILY FOR FASTER TESTING - THIS TAKES ~30 seconds.
    """
    def test_typecountdict_fulldeck(self):
        d = deck.Deck()
        combosof5 = combos.get_combolist(d.cards, 5)
        type_count = combos.typecount_dict(combosof5)

        # Run individual tests
        self.typecountdict_fulldeck_10keys(type_count)
        self.typecountdict_fulldeck_4royalflush(type_count)
        self.typecountdict_fulldeck_40straightflush(type_count)
        self.typecountdict_fulldeck_624quads(type_count)
        self.typecountdict_fulldeck_3744fullhouse(type_count)
    """
    def typecountdict_fulldeck_10keys(self, type_count):
        expected = 10
        result = len(type_count.keys())
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_4royalflush(self, type_count):
        expected = 4
        result = type_count['ROYAL FLUSH']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_40straightflush(self, type_count):
        expected = 36
        result = type_count['STRAIGHT FLUSH']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_624quads(self, type_count):
        expected = 624
        result = type_count['QUADS']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_3744fullhouse(self, type_count):
        expected = 3744
        result = type_count['FULL HOUSE']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_5108flush(self, type_count):
        expected = 5108
        result = type_count['FLUSH']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_10200straight(self, type_count):
        expected = 10200
        result = type_count['STRAIGHT']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_54912sets(self, type_count):
        expected = 54912
        result = type_count['SET']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_123552twopair(self, type_count):
        expected = 123552
        result = type_count['TWO PAIR']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_1098240pairs(self, type_count):
        expected = 1098240
        result = type_count['PAIR']
        self.assertEqual(expected, result)

    def typecountdict_fulldeck_1302540(self, type_count):
        expected = 1302540
        result = type_count['HIGH CARD']
        self.assertEqual(expected, result)

    """
    Tests for get_unique_5cardhands()
    """

    """
    Tests for sort_handslist(handdict)
    """

    """
    Tests for print_unique_5cardhands(handlist)
    """
    # No tests needed, only displays results.

    """
    Tests for count_all_handtypes(combolist)
    """

    """
    Tests for enumerate_unique_5cardhands(combolist)
    """
