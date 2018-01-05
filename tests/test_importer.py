from unittest import TestCase
from pyperlib import importer, coins


class TestBaseImporter(TestCase):
    """A TestCase that creates BaseImporters and verifies their output."""

    def do_test(self, i, w, v, a, **kwargs):
        """Uses importer i with **kwargs, checking that the results fit."""
        coin = i.run(**kwargs)
        self.assertIsInstance(coin, coins.BaseCoin)

        if w is not None:
            self.assertEqual(w, coin.wif_string())
        if v is not None:
            self.assertEqual(v, coin.view_string())
        if a is not None:
            self.assertEqual(a, coin.addr_string())

    def test_all(self):
        """Run do_test with various args to check all cases."""
        cl = coins.CoinList()
        Coin = cl.get_coin("btc")
        i = importer.BaseImporter(Coin)

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        for j in range(10):
            self.do_test(i, None, None, None)  # Generation

        self.do_test(i, wif, None, addr, wif=wif)
        self.do_test(i, None, None, addr, addr=addr)
