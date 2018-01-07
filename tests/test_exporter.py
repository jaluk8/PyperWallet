from unittest import TestCase
from unittest.mock import patch
from pyperlib import exporter, coins


class TestBaseExporter(TestCase):
    """Tests if exporting coins to python values works."""

    cf = coins.CoinFactory()
    Coin = cf.get_coin("btc")

    def do_test(self, e, c, w, v, a):
        """Run exporting on Coin c with e, and checks the result."""
        exported = e.run(c)

        self.assertEqual(w, exported.wif)
        self.assertEqual(a, exported.addr)

    def test_all(self):
        """Run do_test with all test sets."""
        e = exporter.BaseExporter()

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        self.do_test(e, self.Coin(wif=wif), wif, None, addr)
        self.do_test(e, self.Coin(addr=addr), None, None, addr)


class TestCliExporter(TestBaseExporter):
    """Same as TestBaseExporter, but for the Cli exporter."""

    maxDiff = None
    out = ""
    correct_out = """
Coin name: Bitcoin
Compressed: True

Private WIF key: KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU
Private hex key: 3C5F262F56AF74A2C314354BE7EA0CCAFEDA1C059E2B5B3B4C3151912C774\
F78

Public address: 1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx
Public hex key: 02FF136594F723F047A0917A8EC66B56079841AC989FB4F6AC75982FC7F57E\
980A

Coin name: Bitcoin
Compressed: True

Public address: 1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx
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
        e = exporter.CliExporter()

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        self.do_test(e, self.Coin(wif=wif))
        self.do_test(e, self.Coin(addr=addr))

        self.assertEqual(self.correct_out, self.out)
