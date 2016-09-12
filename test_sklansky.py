import unittest
import pokerhands
import sklansky


class TestSklansky(unittest.TestCase):
    """
    Tests for get_group(cardrep):
    """
    # AA in in group 1
    def test_getgroup_AA_returns1(self):
        handrep, expected = 'AA', 1
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # AKs is in group 1
    def test_getgroup_AKs_returns1(self):
        handrep, expected = 'AKs', 1
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # AKo is in group 2
    def test_getgroup_AKo_returns2(self):
        handrep, expected = 'AKo', 2
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # AK in ?
    def test_getgroup_AK_returns2(self):
        handrep, expected = 'AK', 2
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # JTs is in group 3
    def test_getgroup_JTs_returns3(self):
        handrep, expected = 'JTs', 3
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # J9s is in group 4
    def test_getgroup_J9s_returns4(self):
        handrep, expected = 'J9s', 4
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # JT is in group 5
    def test_getgroup_JT_returns5(self):
        handrep, expected = 'JTo', 5
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # 55 is in group 6
    def test_getgroup_55_returns6(self):
        handrep, expected = '55', 6
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # 53s is in group 7
    def test_getgroup_53s_returns7(self):
        handrep, expected = '53s', 7
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # 87o is in group 8
    def test_getgroup_87_returns8(self):
        handrep, expected = '87o', 8
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    # J4 is not in any group
    def test_getgroup_J4_returnsNeg1(self):
        handrep, expected = 'J4', -1
        result = sklansky.get_group(handrep)
        self.assertEqual(expected, result)

    def test_getgroup_AsKs_returns1(self):
        cards = pokerhands.make('AKs')
        expected = 1
        result = sklansky.get_group(cards)
        self.assertEqual(expected, result)

    def test_percentile_group1_returns2percent(self):
        expected = 2
        result = sklansky.percentile(1)
        self.assertEqual(expected, result)
