from unittest import TestCase
from unittest.mock import patch
from pyperlib import exporter, coins


class TestBaseExporter(TestCase):
    """Tests if exporting coins to python values works."""

    def do_test(self, e, c, w, v, a):
        """Run exporting on Coin c with e, and checks the result."""
        wif, view, addr = e.run(c)

        self.assertEqual(w, wif)
        self.assertEqual(v, view)
        self.assertEqual(a, addr)

    def test_all(self):
        """Run do_test with all test sets."""
        cl = coins.CoinList()
        Coin = cl.get_coin("btc")
        e = exporter.BaseExporter()

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        self.do_test(e, Coin(wif=wif), wif, None, addr)
        self.do_test(e, Coin(addr=addr), None, None, addr)
