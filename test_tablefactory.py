import unittest
import table_factory
import session_factory


class TestTableFactory(unittest.TestCase):
    def setUp(self):
        self.pool = session_factory.make_playerpool(quantity=10)

    """
    Tests for factory(**new_config)
    """
    def test_factory_noseatspassed_raisesException(self):
        self.assertRaises(ValueError, table_factory.factory)

    def test_factory_noplayerpool_defaultplayersused(self):
        t = table_factory.factory(seats=2)
        expected = 2
        result = len(t.get_players())
        self.assertEqual(expected, result)

    def test_factory_namedPonyville_hasName(self):
        name = 'Ponyville'
        t = table_factory.factory(seats=2, tablename=name)
        expected = name
        result = t.name
        self.assertEqual(expected, result)

    def test_factory_2seat_Tablehas2seats(self):
        #  import pdb; pdb.set_trace() #BREAKPOINT<C-C.
        t = table_factory.factory(seats=2, playerpool=self.pool)
        expected = 2
        result = len(t)
        self.assertEqual(expected, result)

    def test_factory_3seats_Tablehas3seats(self):
        t = table_factory.factory(seats=3, playerpool=self.pool)
        expected = 3
        result = len(t)
        self.assertEqual(expected, result)

    def test_factory_4seats_Tablehas4seats(self):
        t = table_factory.factory(seats=4, playerpool=self.pool)
        expected = 4
        result = len(t)
        self.assertEqual(expected, result)

    # #########################################################
    def test_factory_2seat_seat0bankminusStack(self):
        t = table_factory.factory(seats=2, playerpool=self.pool)
        expected = session_factory.CPU_BANK_BITS - table_factory.DEF_STACK
        result = t.seats[0].player.bank
        self.assertEqual(expected, result)

    def test_factory_2seat_seat1bankminusStack(self):
        t = table_factory.factory(seats=2, playerpool=self.pool)
        expected = session_factory.CPU_BANK_BITS - table_factory.DEF_STACK
        result = t.seats[1].player.bank
        self.assertEqual(expected, result)

    def test_factory_2seats_tablehas2players(self):
        t = table_factory.factory(seats=2, playerpool=self.pool)
        expected = 2
        result = len(t.get_players())
        self.assertEqual(expected, result)

    def test_factory_2seats_seat0hasstack(self):
        t = table_factory.factory(seats=2, playerpool=self.pool)
        expected = table_factory.DEF_STACK
        result = t.seats[0].stack
        self.assertEqual(expected, result)

    def test_factory_2seats_seat1hasstack(self):
        t = table_factory.factory(seats=2, playerpool=self.pool)
        expected = table_factory.DEF_STACK
        result = t.seats[1].stack
        self.assertEqual(expected, result)

    def test_factory_3seats_Tablehas3players(self):
        t = table_factory.factory(seats=3, playerpool=self.pool)
        expected = 3
        result = len(t.get_players())
        self.assertEqual(expected, result)

    def test_factory_2stepstacks_seat0has100(self):
        t = table_factory.factory(seats=2, stepstacks=True, playerpool=self.pool)
        expected = 100
        result = t.seats[0].stack
        self.assertEqual(expected, result)

    def test_factory_2stepstacks_seat1has200(self):
        t = table_factory.factory(seats=2, stepstacks=True, playerpool=self.pool)
        expected = 200
        result = t.seats[1].stack
        self.assertEqual(expected, result)

    def test_factory_2seats_stack666_seat0hasstack666(self):
        newstack = 666
        t = table_factory.factory(seats=2, stack=newstack, playerpool=self.pool)
        result = t.seats[0].stack
        self.assertEqual(newstack, result)

    def test_factory_2seats_stack666_seat1hasstack666(self):
        newstack = 666
        t = table_factory.factory(seats=2, stack=newstack, playerpool=self.pool)
        result = t.seats[1].stack
        self.assertEqual(newstack, result)

    def test_factory_variance50prcnt_nostacklowerthan500(self):
        vary = .50
        low = 500
        t = table_factory.factory(seats=8, variance=vary, playerpool=self.pool)
        self.assertTrue(min(t.stacklist()) >= low)

    def test_factory_variance50prcnt_nostackhigherthan1500(self):
        vary = .50
        hi = 1500
        t = table_factory.factory(seats=8, variance=vary, playerpool=self.pool)
        self.assertTrue(min(t.stacklist()) <= hi)

    def test_factory_2seats_remove0_1player(self):
        t = table_factory.factory(seats=2, remove=0, playerpool=self.pool)
        expected = 1
        result = len(t.get_players())
        self.assertEqual(expected, result)
