import unittest
import player
import factory


class TestTableFactory(unittest.TestCase):
    def setUp(self):
        self.pool = factory.make_playerpool(quantity=10)

    """
    Tests for table_factory(**new_config)
    """
    def test_tablefactory_noseatspassed_raisesException(self):
        self.assertRaises(ValueError, factory.table_factory)

    def test_tablefactory_noplayerpool_defaultplayersused(self):
        t = factory.table_factory(seats=2)
        expected = 2
        result = len(t.get_players())
        self.assertEqual(expected, result)

    def test_tablefactory_namedPonyville_hasName(self):
        name = 'Ponyville'
        t = factory.table_factory(seats=2, tablename=name)
        expected = name
        result = t.name
        self.assertEqual(expected, result)

    def test_tablefactory_2seat_Poolhas2less(self):
        poolsize = len(self.pool)
        factory.table_factory(seats=2, playerpool=self.pool)
        expected = 2
        result = poolsize - len(self.pool)
        self.assertEqual(expected, result)

    def test_tablefactory_2seat_Tablehas2seats(self):
        t = factory.table_factory(seats=2, playerpool=self.pool)
        expected = 2
        result = len(t)
        self.assertEqual(expected, result)

    def test_tablefactory_3seats_Tablehas3seats(self):
        t = factory.table_factory(seats=3, playerpool=self.pool)
        expected = 3
        result = len(t)
        self.assertEqual(expected, result)

    def test_tablefactory_4seats_Tablehas4seats(self):
        t = factory.table_factory(seats=4, playerpool=self.pool)
        expected = 4
        result = len(t)
        self.assertEqual(expected, result)

    # #########################################################
    def test_tablefactory_2seat_seat0bankminusStack(self):
        t = factory.table_factory(seats=2, playerpool=self.pool)
        expected = factory.CPU_BANK_BITS - factory.DEF_STACK
        result = t.seats[0].player.bank
        self.assertEqual(expected, result)

    def test_tablefactory_2seat_seat1bankminusStack(self):
        t = factory.table_factory(seats=2, playerpool=self.pool)
        expected = factory.CPU_BANK_BITS - factory.DEF_STACK
        result = t.seats[1].player.bank
        self.assertEqual(expected, result)

    def test_tablefactory_2seats_tablehas2players(self):
        t = factory.table_factory(seats=2, playerpool=self.pool)
        expected = 2
        result = len(t.get_players())
        self.assertEqual(expected, result)

    def test_tablefactory_2seats_seat0hasstack(self):
        t = factory.table_factory(seats=2, playerpool=self.pool)
        expected = factory.DEF_STACK
        result = t.seats[0].stack
        self.assertEqual(expected, result)

    def test_tablefactory_2seats_seat1hasstack(self):
        t = factory.table_factory(seats=2, playerpool=self.pool)
        expected = factory.DEF_STACK
        result = t.seats[1].stack
        self.assertEqual(expected, result)

    def test_tablefactory_3seats_Tablehas3players(self):
        t = factory.table_factory(seats=3, playerpool=self.pool)
        expected = 3
        result = len(t.get_players())
        self.assertEqual(expected, result)

    def test_tablefactory_2stepstacks_seat0has100(self):
        t = factory.table_factory(seats=2, stepstacks=True, playerpool=self.pool)
        expected = 100
        result = t.seats[0].stack
        self.assertEqual(expected, result)

    def test_tablefactory_2stepstacks_seat1has200(self):
        t = factory.table_factory(seats=2, stepstacks=True, playerpool=self.pool)
        expected = 200
        result = t.seats[1].stack
        self.assertEqual(expected, result)

    def test_tablefactory_2seats_stack666_seat0hasstack666(self):
        newstack = 666
        t = factory.table_factory(seats=2, stack=newstack, playerpool=self.pool)
        result = t.seats[0].stack
        self.assertEqual(newstack, result)

    def test_tablefactory_2seats_stack666_seat1hasstack666(self):
        newstack = 666
        t = factory.table_factory(seats=2, stack=newstack, playerpool=self.pool)
        result = t.seats[1].stack
        self.assertEqual(newstack, result)

    def test_tablefactory_variance50prcnt_nostacklowerthan500(self):
        vary = .50
        low = 500
        t = factory.table_factory(seats=8, variance=vary, playerpool=self.pool)
        self.assertTrue(min(t.stacklist()) >= low)

    def test_tablefactory_variance50prcnt_nostackhigherthan1500(self):
        vary = .50
        hi = 1500
        t = factory.table_factory(seats=8, variance=vary, playerpool=self.pool)
        self.assertTrue(min(t.stacklist()) <= hi)

    def test_tablefactory_2seats_remove0_1player(self):
        t = factory.table_factory(seats=2, remove=0, playerpool=self.pool)
        expected = 1
        result = len(t.get_players())
        self.assertEqual(expected, result)


class TestSessionFactory(unittest.TestCase):
    def setUp(self):
        # Make a default hero
        self.h = player.Player('Octavia', playertype="HUMAN")
        self.h.deposit(factory.CPU_BANK_BITS)

    """
    Tests for session_factory(**new_config)
    """
    def test_sessionfactory_noseatspassed_raisesException(self):
        self.assertRaises(ValueError, factory.session_factory)

    def test_sessionfactory_2seat_Poolhas2less(self):
        s = factory.session_factory(seats=2, game="FIVE CARD STUD")
        expected = 2
        result = factory.DEFAULT_POOL - len(s.playerpool)
        self.assertEqual(expected, result)

    def test_sessionfactory_hero_defaultseat_seat0(self):
        s = factory.session_factory(seats=2, game="FIVE CARD STUD",
                                    hero=self.h, herobuyin=factory.DEF_STACK)
        expected = 0
        result = s._table.get_index(self.h)
        self.assertEqual(expected, result)

    def test_sessionfactory_hero_defaultseat_seat0hashero(self):
        s = factory.session_factory(seats=2, game="FIVE CARD STUD",
                                    hero=self.h, herobuyin=factory.DEF_STACK)
        expected = self.h.name
        result = str(s._table.seats[0].player)
        self.assertEqual(expected, result)

    def test_sessionfactory_hero_herohasbankminusstack(self):
        s = factory.session_factory(seats=2, game="FIVE CARD STUD",
                                    hero=self.h, herobuyin=factory.DEF_STACK)
        expected = factory.CPU_BANK_BITS - factory.DEF_STACK
        result = s._table.seats[0].player.bank
        self.assertEqual(expected, result)


class TestMakePlayerpool(unittest.TestCase):
    """
    Tests for make_playerpool(**new_config)
    """
    # No quantity pass
    def test_makeplayerpool_noquantity_raisesException(self):
        self.assertRaises(ValueError, factory.make_playerpool)

    # 1 player
    def test_makeplayerpool_qty1_len1(self):
        pool = factory.make_playerpool(quantity=1)
        expected = 1
        result = len(pool)
        self.assertEqual(expected, result)

    # 1 player has the DEPOSIT amt
    def test_makeplayerpool_qty1_hasbank(self):
        pool = factory.make_playerpool(quantity=1)
        expected = factory.CPU_BANK_BITS
        result = pool[0].bank
        self.assertEqual(expected, result)

    # 1 player, is the pass playertype
    def test_makeplayerpool_1FISH_isFISH(self):
        ptype = 'FISH'
        pool = factory.make_playerpool(quantity=1, types=ptype)
        expected = ptype
        result = pool[0].playertype
        self.assertEqual(expected, result)

    # 1 player, named 'bob0'
    def test_makeplayerpool_1defaultname_isbob0(self):
        pool = factory.make_playerpool(quantity=1)
        expected = 'bob0'
        result = pool[0].name
        self.assertEqual(expected, result)

    # 10 players
    def test_makeplayerpool_qty10_len10(self):
        pool = factory.make_playerpool(quantity=10)
        expected = 10
        result = len(pool)
        self.assertEqual(expected, result)

    # 10 players, bobs, test last name
    def test_makeplayerpool_10bobs_lastisbob9(self):
        pool = factory.make_playerpool(quantity=10)
        expected = 'bob9'
        result = pool[-1].name
        self.assertEqual(expected, result)

    # 10 players, random names, all unique
    def test_makeplayerpool_10random_allunique(self):
        pool = factory.make_playerpool(quantity=10, names='random')
        expected = 10
        result = len(set([p.name for p in pool]))
        self.assertEqual(expected, result)
