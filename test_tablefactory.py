import unittest
import table_factory


class TestTableFactory(unittest.TestCase):
    """
    Tests for factory(**new_config)
    """
    def test_factory_2seat_Tablehas2seats(self):
        t = table_factory.factory(seats=2)
        expected = 2
        result = len(t)
        self.assertEqual(expected, result)

    def test_factory_2seat_seat0bankminusStack(self):
        t = table_factory.factory(seats=2)
        expected = table_factory.DEPOSIT - table_factory.DEF_STACK
        result = t.seats[0].player.bank
        self.assertEqual(expected, result)

    def test_factory_2seat_seat1bankminusStack(self):
        t = table_factory.factory(seats=2)
        expected = table_factory.DEPOSIT - table_factory.DEF_STACK
        result = t.seats[1].player.bank
        self.assertEqual(expected, result)

    def test_factory_2seats_tablehas2players(self):
        t = table_factory.factory(seats=2)
        expected = 2
        result = len(t.get_players())
        self.assertEqual(expected, result)

    def test_factory_2seats_seat0hasstack(self):
        t = table_factory.factory(seats=2)
        expected = table_factory.DEF_STACK
        result = t.seats[0].stack
        self.assertEqual(expected, result)

    def test_factory_2seats_seat1hasstack(self):
        t = table_factory.factory(seats=2)
        expected = table_factory.DEF_STACK
        result = t.seats[1].stack
        self.assertEqual(expected, result)

    def test_factory_3seats_Tablehas3seats(self):
        t = table_factory.factory(seats=3)
        expected = 3
        result = len(t)
        self.assertEqual(expected, result)

    def test_factory_3seats_Tablehas3players(self):
        t = table_factory.factory(seats=3)
        expected = 3
        result = len(t.get_players())
        self.assertEqual(expected, result)

    def test_factory_hero_defaultseat0(self):
        name = 'Octavia'
        t = table_factory.factory(seats=2, heroname=name)
        result = str(t.seats[0].player)
        self.assertEqual(name, result)

    def test_factory_hero_herohasbankminusstack(self):
        t = table_factory.factory(seats=2)
        expected = table_factory.DEPOSIT - table_factory.DEF_STACK
        result = t.seats[0].player.bank
        self.assertEqual(expected, result)

    def test_factory_2stepstacks_seat0has100(self):
        t = table_factory.factory(seats=2, stepstacks=True)
        expected = 100
        result = t.seats[0].stack
        self.assertEqual(expected, result)

    def test_factory_2stepstacks_seat1has200(self):
        t = table_factory.factory(seats=2, stepstacks=True)
        expected = 200
        result = t.seats[1].stack
        self.assertEqual(expected, result)

    def test_factory_2seats_stack666_seat0hasstack666(self):
        newstack = 666
        t = table_factory.factory(seats=2, stack=newstack)
        result = t.seats[0].stack
        self.assertEqual(newstack, result)

    def test_factory_2seats_stack666_seat1hasstack666(self):
        newstack = 666
        t = table_factory.factory(seats=2, stack=newstack)
        result = t.seats[1].stack
        self.assertEqual(newstack, result)
