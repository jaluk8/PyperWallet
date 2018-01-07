from unittest import TestCase
from unittest.mock import patch
from pyperlib import importer, coins, helper


class TestImporterFactory(helper.TestNameFactory):
    """Test the ImporterFactory's get method."""

    factory = importer.ImporterFactory

    def test_all(self):
        """Attempt to import various names."""
        self.do_test("Base", None)
        self.do_test("Nonexistant", None)
        self.do_test("cli", importer.CliImporter)


class TestBaseImporter(TestCase):
    """A TestCase that creates BaseImporters and verifies their output."""

    cf = coins.CoinFactory()
    Coin = cf.get_coin("btc")

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
        i = importer.BaseImporter(self.Coin)

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
        i = importer.GenImporter(self.Coin)

        for j in range(10):
            self.do_test(i, None, None, None)


class TestCliImporter(TestBaseImporter):
    """The same as TestBaseImporter, but for CliImporter."""

    def test_all(self):
        """Run do_test given command line input."""
        i = importer.CliImporter(self.Coin)

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
        i = importer.BaseBrainImporter(self.Coin)

        phrase = "pyperwalletbrain"
        wif = "KxiDxGBdavV586DaKPAZfA8rB8jpjxXjEhQ6fhSZmZpbhNkX7FLb"
        addr = "1Ge1Cn5UzqNnx37bpnoqWEY4McPFGG8Z5f"

        self.do_test(i, wif, None, addr, brain=phrase)
