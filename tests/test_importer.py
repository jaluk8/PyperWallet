from unittest import TestCase
from unittest.mock import patch
from pyperlib import importer, coins


class TestBaseImporter(TestCase):
    """A TestCase that creates BaseImporters and verifies their output."""

    def do_test(self, i, w, v, a, *args, **kwargs):
        """Uses importer i with given args, checking that the results fit."""
        coin = i.run(*args, **kwargs)
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


class TestGenImporter(TestBaseImporter):
    """The same as TestBaseImporter, but for GenImporter."""

    def test_all(self):
        """Run do_test a couple times to test generation."""

        cl = coins.CoinList()
        Coin = cl.get_coin("btc")
        i = importer.GenImporter(Coin)

        for j in range(10):
            self.do_test(i, None, None, None)


class TestCliImporter(TestBaseImporter):
    """The same as TestBaseImporter, but for CliImporter."""

    def test_all(self):
        """Run do_test given command line input."""

        cl = coins.CoinList()
        Coin = cl.get_coin("btc")
        i = importer.CliImporter(Coin)

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        in1 = ["wif", wif]
        in2 = ["addr", addr]

        with patch("builtins.input", side_effect=in1):
            self.do_test(i, wif, None, addr)

        with patch("builtins.input", side_effect=in2):
            self.do_test(i, None, None, addr)

class TestBaseBrainImporter(TestBaseImporter):
    """The same as TestBaseImporter, but for BaseBrainImporter."""

    def test_all(self):
        """Run do_test for a brain phrase."""

        cl = coins.CoinList()
        Coin = cl.get_coin("btc")
        i = importer.BaseBrainImporter(Coin)

        phrase = "pyperwalletbrain"
        wif = "KxiDxGBdavV586DaKPAZfA8rB8jpjxXjEhQ6fhSZmZpbhNkX7FLb"
        addr = "1Ge1Cn5UzqNnx37bpnoqWEY4McPFGG8Z5f"

        self.do_test(i, wif, None, addr, brain=phrase)
