import unittest
import game


def addone(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(addone(3), 4)
