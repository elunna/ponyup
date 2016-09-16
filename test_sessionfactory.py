import unittest
import session_factory
import table_factory


class TestSessionFactory(unittest.TestCase):
    """
    Tests for factory(**new_config)
    """
    def test_factory_noseatspassed_raisesException(self):
        self.assertRaises(ValueError, session_factory.factory)

    def test_factory_hero_heroseat0(self):
        name = 'Octavia'
        s = session_factory.factory(seats=2, game="FIVE CARD STUD",
                                    heroname=name, heroseat=0)
        result = str(s._table.seats[0].player)
        self.assertEqual(name, result)

    def test_factory_hero_herohasbankminusstack(self):
        s = session_factory.factory(seats=2, game="FIVE CARD STUD",
                                    heroname='Octavia', heroseat=0)
        expected = table_factory.DEPOSIT - table_factory.DEF_STACK
        result = s._table.seats[0].player.bank
        self.assertEqual(expected, result)

    """
    Tests for make_playerpool(**new_config)
    """
    # No quantity pass
    def test_makeplayerpool_noquantity_raisesException(self):
        self.assertRaises(ValueError, session_factory.make_playerpool)

    # 1 player
    def test_makeplayerpool_qty1_len1(self):
        pool = session_factory.make_playerpool(quantity=1)
        expected = 1
        result = len(pool)
        self.assertEqual(expected, result)

    # 1 player has the DEPOSIT amt
    def test_makeplayerpool_qty1_hasbank(self):
        pool = session_factory.make_playerpool(quantity=1)
        expected = table_factory.DEPOSIT
        result = pool[0].bank
        self.assertEqual(expected, result)

    # 1 player, is the pass playertype
    def test_makeplayerpool_1FISH_isFISH(self):
        ptype = 'FISH'
        pool = session_factory.make_playerpool(quantity=1, types=ptype)
        expected = ptype
        result = pool[0].playertype
        self.assertEqual(expected, result)

    # 1 player, named 'bob0'
    def test_makeplayerpool_1defaultname_isbob0(self):
        pool = session_factory.make_playerpool(quantity=1)
        expected = 'bob0'
        result = pool[0].name
        self.assertEqual(expected, result)

    # 10 players
    def test_makeplayerpool_qty10_len10(self):
        pool = session_factory.make_playerpool(quantity=10)
        expected = 10
        result = len(pool)
        self.assertEqual(expected, result)

    # 10 players, bobs, test last name
    def test_makeplayerpool_10bobs_lastisbob9(self):
        pool = session_factory.make_playerpool(quantity=10)
        expected = 'bob9'
        result = pool[-1].name
        self.assertEqual(expected, result)

    # 10 players, random names, all unique
    def test_makeplayerpool_10random_allunique(self):
        pool = session_factory.make_playerpool(quantity=10, names='random')
        expected = 10
        result = len(set([p.name for p in pool]))
        self.assertEqual(expected, result)
