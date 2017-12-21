from pyperlib import coins
from unittest import TestCase

class TestCoinList(TestCase):
    """A TestCase for the CoinList class."""

    def do_test(self, name, cl):
        """Check that the coinlist has the coin and can load it."""
        self.assertTrue(cl.has_coin(name))
        try:
            c = cl.get_coin(name)
        except NotImplementedError:
            return
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

    example_keys = {
        "btc": ("KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU", None, "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"),
        "ltc": ("T3hvqLBBEtBui8Leo9bhezChRggpouqVxBP2A9svN8gYrig13GDZ", None, "LWUhrUrbUMZTsNqQkCtuMwsr9pTskCLtVt")}
    
    def check_load(self, Coin, wif, view, addr):
        """Load Coin from various keys and check correctness."""
        wif = Coin.str2wif(wif)
        addr = Coin.str2addr(addr)
        if Coin.has_privacy:
            view = Coin.str2view()

        c1 = Coin(wif=wif)
        self.assertEqual(c1.wif(), wif)
        self.assertEqual(c1.addr(), addr)
        if Coin.has_privacy:
            self.assertEqual(c1.view(), view)

        if Coin.load_from_addr:
            c2 = Coin(addr=addr)
            self.assertEqual(c2.wif(), None)
            self.assertEqual(c2.addr(), addr)
            if Coin.has_privacy:
                self.assertEqual(c2.view(), None)

        if Coin.has_privacy:
            c3 = Coin(view=view)
            self.assertEqual(c3.wif(), None)
            self.assertEqual(c3.addr(), addr)
            self.assertEqual(c3.view(), view)

    def test_all(self):
        """Gets a list of all implemented coins and runs check_coin."""
        cl = coins.CoinList()
        for name in cl.list_coins():
            if name in self.example_keys:
                Coin = cl.get_coin(name)
                key = self.example_keys[name]
                self.check_load(Coin, *key)
