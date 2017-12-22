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
        self.do_test('ltc', cl)


class TestBaseCoin(TestCase):
    """A TestCase for the BaseCoin class."""

    def do_constructor(self, *args, **kwargs):
        """Check that the constructor throws the correct error."""
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
        "btc": ("KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU",
                None, "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"),
        "ltc": ("T3hvqLBBEtBui8Leo9bhezChRggpouqVxBP2A9svN8gYrig13GDZ",
                None, "LWUhrUrbUMZTsNqQkCtuMwsr9pTskCLtVt"),
        "bch": ("5JNrhoR2HJ1fH5ts1n2D77o35MrWCEj3gQvBWTc3oZi55uuMu34",
                None, "13gU9r4cKRvLMKgFtt5nuMYJ6SEyPBjwid"),  # Uncompressed
        "dash": ("XCZtcGqHxmFAmLxQhKmra9AwkESEHknu5jTAKEgSTAFypc93jovp",
                 None, "XwEMaB6n2CpxKS9poY1DZCZEv7v8woJmWu"),
        "doge": ("QWyapnA2914T89HSR23QZiJgmM55oPeBUcjdJ9PkFKYccZpoF9uj",
                 None, "DFxKgD7CY6zTGDGsyFfr2YHNzPhMooUSYb"),
        "ftc": ("N9mVytYSm1cDEecUKv68mis5WF8cC9Xzi6nwMm9GAExJ4wmNDU6d",
                None, "6fQZRM3i5NWs5YXEdQgAKpjrGfwjZQnbje"),
        "vtc": ("WZHPcZNDbWiJEUEgR36prdAR2nqJ1ZftFNRnnjUV5N2SkeVgVkMk",
                None, "VmeQa8L2xidM976jLbBqCWPWFbEDEXfPpe"),
        "zec": ("Kx62UU7eJP4rCtaU1N8zy34cWnkj2CoFfPbetMbSD9hoY1gDLvdL",
                None, "t1WCf2xoYaeUzHKjdLCxjHL2c4W2S6jZMSQ")}

    def check_gen(self, Coin):
        """Generate Coin and check that it loads correctly."""
        for _ in range(100):
            c = Coin()

            if Coin.has_privacy:
                view = c.view
            else:
                view = None

            self.check_load(Coin, c.wif, view, c.addr)

    def check_load(self, Coin, wif, view, addr):
        """Load Coin from various keys and check correctness."""
        c1 = Coin(wif=wif)
        self.assertEqual(c1.wif, wif)
        self.assertEqual(c1.addr, addr)
        if Coin.has_privacy:
            self.assertEqual(c1.view, view)

        if Coin.load_from_addr:
            c2 = Coin(addr=addr)
            self.assertEqual(c2.wif, None)
            self.assertEqual(c2.addr, addr)
            if Coin.has_privacy:
                self.assertEqual(c2.view, None)

        if Coin.has_privacy:
            c3 = Coin(view=view)
            self.assertEqual(c3.wif, None)
            self.assertEqual(c3.addr, addr)
            self.assertEqual(c3.view, view)

    def get_key(self, name, Coin):
        """Retrieves the example values for name."""
        key = self.example_keys[name]

        wif = Coin.str2wif(key[0])
        addr = Coin.str2addr(key[2])
        if Coin.has_privacy:
            view = Coin.str2view(key[1])
        else:
            view = None

        return wif, view, addr

    def test_all(self):
        """Gets a list of all implemented coins and runs check_coin."""
        cl = coins.CoinList()
        for name in cl.list_coins():
            Coin = cl.get_coin(name)
            self.check_gen(Coin)

            if name in self.example_keys:
                key = self.get_key(name, Coin)
                self.check_load(Coin, *key)
