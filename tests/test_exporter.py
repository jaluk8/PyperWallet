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


class TestCliExporter(TestCase):
    """Same as TestBaseExporter, but for the Cli exporter."""

    out = ""
    correct_out = """
Coin type: Bitcoin
WIF: KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU
Address: 1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx

Coin type: Bitcoin
Address: 1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx
"""

    def mock_print(self):
        """Creates the mock print function."""
        def print(x):
            """Record the input in self.out."""
            self.out += x + "\n"
        return print

    def do_test(self, e, c):
        """Run exporting on Coin c with e, and records the output."""
        self.out += '\n'
        with patch('builtins.print', new_callable=self.mock_print):
            e.run(c)

    def test_all(self):
        """Run do_test with all test sets."""
        cl = coins.CoinList()
        Coin = cl.get_coin("btc")
        e = exporter.CliExporter()

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        self.do_test(e, Coin(wif=wif))
        self.do_test(e, Coin(addr=addr))

        self.assertEqual(self.correct_out, self.out)
