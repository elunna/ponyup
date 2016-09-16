import unittest
import session_factory


class TestSessionFactory(unittest.TestCase):
    """
    Tests for factory(**new_config)
    """
    def test_factory_noseatspassed_raisesException(self):
        self.assertRaises(ValueError, session_factory.factory)

    def test_factory_namedPonyville_hasName(self):
        name = 'Ponyville'
        t = session_factory.factory(seats=2, game="FIVE CARD STUD", tablename=name)
        expected = name
        result = t.tablename
        self.assertEqual(expected, result)

    """
    Tests for make_playerpool(**new_config)
    """
