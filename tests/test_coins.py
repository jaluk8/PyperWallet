from pyperlib import coins
from unittest import TestCase

class TestCoinList(TestCase):
    """A TestCase for the CoinList class."""

    def do_test(self, name, cl):
        """Check that the coinlist has the coin and can load it."""
        self.assertTrue(cl.has_coin(name))
        c = cl.get_coin(name)
        self.assertTrue(issubclass(c, coins.BaseCoin))
    def tests(self):
        """Check all coins in the list, as well as the current top 3."""
        cl = coins.CoinList()
        for name in cl.list_coins():
            self.do_test(name, cl)
        self.do_test('btc', cl)
        self.do_test('eth', cl)
        self.do_test('ltc', cl)

class TestBaseCoin(TestCase):
    """A TestCase for the BaseCoin class."""

    def do_constructor(self, *args, **kwargs):
        """Check that the constructor does not error something other than NotImplementedError."""
        self.assertRaises(NotImplementedError, coins.BaseCoin, *args, **kwargs)

    def test_set(self):
        """Check all possible versions of the constructor."""
        self.do_constructor()
        self.do_constructor(wif=1)
        self.do_constructor(view=1)
        self.do_constructor(addr=1)

class TestAllCoins(TestCase):
    """A TestCase for every Coin module."""
