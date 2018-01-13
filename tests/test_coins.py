from pyperlib import coins, data
from unittest import TestCase


class TestCoinFactory(TestCase):
    """A TestCase for the CoinFactory class."""

    def do_test(self, name, cf):
        """Check that the coinfactory has the coin and can load it."""
        self.assertTrue(cf.has(name))
        try:
            c = cf.get(name)
        except NotImplementedError:
            return
        self.assertTrue(issubclass(c, coins.BaseCoin))

    def tests(self):
        """Check all coins in the list, as well as the current top 3."""
        cf = coins.CoinFactory()
        for name in cf.list():
            self.do_test(name, cf)
        self.do_test('bitcoin', cf)
        self.do_test('litecoin', cf)


class TestBaseCoin(TestCase):
    """A TestCase for the BaseCoin class."""

    def do_constructor(self, *args, **kwargs):
        """Check that the constructor throws the correct error."""
        self.assertRaises(NotImplementedError, coins.BaseCoin, *args, **kwargs)

    def test_set(self):
        """Check all possible versions of the constructor."""
        self.do_constructor()


class TestAllCoins(TestCase):
    """A TestCase for every Coin module."""

    example_keys = {
        "bitcoin": ("KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU",
                    None, "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"),
        "litecoin": ("T3hvqLBBEtBui8Leo9bhezChRggpouqVxBP2A9svN8gYrig13GDZ",
                     None, "LWUhrUrbUMZTsNqQkCtuMwsr9pTskCLtVt"),
        "bitcoincash": ("5JNrhoR2HJ1fH5ts1n2D77o35MrWCEj3gQvBWTc3oZi55uuMu34",
                        None, "13gU9r4cKRvLMKgFtt5nuMYJ6SEyPBjwid"),
        "dash": ("XCZtcGqHxmFAmLxQhKmra9AwkESEHknu5jTAKEgSTAFypc93jovp",
                 None, "XwEMaB6n2CpxKS9poY1DZCZEv7v8woJmWu"),
        "dogecoin": ("6JDNEPxEquFZs5qEMjHkGAjkGU3VbSiQkGaz7FfDhTwxwd88tL5",
                     None, "DL95V4VvXbvhVdeih8ovaXMHijh2rphiXb"),
        "feathercoin": ("N9mVytYSm1cDEecUKv68mis5WF8cC9Xzi6nwMm9GAExJ4wmNDU6d",
                        None, "6fQZRM3i5NWs5YXEdQgAKpjrGfwjZQnbje"),
        "vertcoin": ("L5f9KLMVxanA7aVANckLmCcCb5T93uBGkiQauDBCVBXfD3JQnH9e",
                     None, "Vy47znT6TubeUnhMau9v4ZuKrDdbfAJHKG"),
        "zcash": ("Kx62UU7eJP4rCtaU1N8zy34cWnkj2CoFfPbetMbSD9hoY1gDLvdL",
                  None, "t1WCf2xoYaeUzHKjdLCxjHL2c4W2S6jZMSQ"),
        "ethereum": ("ab2aeb09578892b1658ee824ae166772c57ce4b77685eca3ea6647da"
                     "84b96287", None, "0xB8F758b3f2016Bb391fb18C7Ef39847ef164"
                     "649e")}

    def check_gen(self, Coin):
        """Generate Coin and check that it loads correctly."""
        for _ in range(100):
            c = Coin()

            self.assertIsInstance(c.wif_string(), str)
            self.assertIsInstance(c.addr_string(), str)

            if Coin.has_privacy:
                view = c.view
                self.assertIsInstance(c.view_string(), str)
            else:
                view = None

            self.check_load(Coin, None, None, None, c.wif, view, c.addr)

    def check_load(self, Coin, wif_str, view_str, addr_str, wif, view, addr):
        """Load Coin from various keys and check correctness."""
        c1 = Coin(key=wif)
        self.assertEqual(c1.wif, wif)
        self.assertEqual(c1.addr, addr)
        if Coin.has_privacy:
            self.assertEqual(c1.view, view)

        c2 = Coin(key=addr)
        self.assertEqual(c2.wif, None)
        self.assertEqual(c2.addr, addr)
        if Coin.has_privacy:
            self.assertEqual(c2.view, None)

        if Coin.has_privacy:
            c3 = Coin(key=view)
            self.assertEqual(c3.wif, None)
            self.assertEqual(c3.addr, None)
            self.assertEqual(c3.view, view)

        if wif_str is not None:
            c4 = Coin(key=wif_str)
            self.assertEqual(c4.wif, wif)

        if addr_str is not None:
            c5 = Coin(key=addr_str)
            self.assertEqual(c5.addr, addr)

        if view_str is not None and Coin.has_privacy:
            c6 = Coin(key=view_str)
            self.assertEqual(c6.view, view)

    def get_key(self, name, Coin):
        """Retrieves the example values for name."""
        key = self.example_keys[name]

        wif = Coin.str2wif(key[0])
        addr = Coin.str2addr(key[2])
        if Coin.has_privacy:
            view = Coin.str2view(key[1])
        else:
            view = None

        return key[0], key[1], key[2], wif, view, addr

    def test_all(self):
        """Gets a list of all implemented coins and runs check_coin."""
        cf = coins.CoinFactory()
        for name in cf.list():
            Coin = cf.get(name)
            self.check_gen(Coin)

            if name in self.example_keys:
                key = self.get_key(name, Coin)
                self.check_load(Coin, *key)


class TestValidation(TestAllCoins):
    """A TestCase for checking that checksum validation works."""

    example_keys = {  # These all have minor errors included
        "bitcoin": ("KyF4khaPVK9YeMBUukYKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU",
                    None, "1PYqAUK4q8Lbq32o32ouyQMUFkzszw6ywx"),
        "litecoin": ("T3hvqLBBEtBui8Leo9bhezChRggpPuqVxBP2A9svN8gYrig13GDZ",
                     None, "LWUhrUrbUMZTsNqQkCtuMwsr9pTskCLrVt"),
        "bitcoincash": ("5JNrhoR2HJ1fH5ts1n2D77o35MrVCEj3gQvBWTc3oZi55uuMu34",
                        None, "13gU9r4cKRvLMKgFtt5nuMYJ6SEyPBjwiD"),
        "dash": ("XCZtcGqHxmFAmfxQhKmra9AwkESEHknu5jTAKEgSTAFypc93jovp",
                 None, "XwEMaB6n2CPxKS9poY1DZCZEv7v8woJmWu"),
        "dogecoin": ("6JDNEPxEquFzs5qEMjHkGAjkGU3VbSiQkGaz7FfDhTwxwd88tL5",
                     None, "DL95V4VvxbvhVdeih8ovaXMHijh2rphiXb"),
        "feathercoin": ("N9mVytYSM1cDEecUKv68mis5WF8cC9Xzi6nwMm9GAExJ4wmNDU6d",
                        None, "6fQZRM4i5NWs5YXEdQgAKpjrGfwjZQnbje"),
        "vertcoin": ("L5f9KLMVxanA6aVANckLmCcCb5T93uBGkiQauDBCVBXfD3JQnH9e",
                     None, "Vy47znT6TubeunhMau9v4ZuKrDdbfAJHKG"),
        "zcash": ("Kx62UU7eJP4rCtaU1N8zy34cWnkj2CoFfpbetMbSD9hoY1gDLvdL",
                  None, "t1WCf2xoYaeUzHKjdLCxjHL2C4W2S6jZMSQ"),
        "ethereum": ("ab2aeb09578892b1658ee924ae166772c57ce4b77685eca3ea6647da"
                     "84b96287", None, "0xB8F758b3f2016Bb391fb18C7EF39847ef164"
                     "649e")}

    def check_gen(self, Coin):
        """Does nothing as gen validation is checked in the base class."""

    def check_load(self, Coin, wif_str, view_str, addr_str, wif, view, addr):
        """Load Coin from various keys and check incorrectness."""

        if Coin.has_priv_csum:
            with self.assertRaises(coins.InvalidCoinError):
                c1 = Coin(key=wif)

        if Coin.has_addr_csum:
            with self.assertRaises(coins.InvalidCoinError):
                c2 = Coin(key=addr)

        if Coin.has_view_csum and Coin.has_privacy:
            with self.assertRaises(coins.InvalidCoinError):
                c3 = Coin(key=view)
