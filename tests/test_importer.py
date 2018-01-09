from unittest import TestCase
from pyperlib import importer, coins, prompter, helper


class TestImporterFactory(helper.TestNameFactory):
    """Test the ImporterFactory's get method."""

    factory = importer.ImporterFactory

    def test_all(self):
        """Attempt to import various names."""
        self.do_test("base", None)
        self.do_test("nonexistant", None)
        self.do_test("wif", importer.WifImporter)


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


class TestCliImporters(TestBaseImporter, helper.CliTestCase):
    """Test wif and addr importers using the CLI prompter."""

    def test_all(self):
        """Run do_test given command line input."""
        w_i = importer.WifImporter(self.Coin, prompter.CliPrompter)
        a_i = importer.AddrImporter(self.Coin, prompter.CliPrompter)

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        in1 = [wif]
        in2 = [addr]

        self.cli_test(self.do_test, stdin=in1, i=w_i, w=wif, v=None, a=addr)
        self.cli_test(self.do_test, stdin=in2, i=a_i, w=None, v=None, a=addr)


class TestBrainImporter(TestBaseImporter):
    """The same as TestBaseImporter, but for BrainImporter."""

    def test_all(self):
        """Run do_test for a brain phrase."""
        i = importer.BrainImporter(self.Coin)

        phrase = "pyperwalletbrain"
        wif = "KxiDxGBdavV586DaKPAZfA8rB8jpjxXjEhQ6fhSZmZpbhNkX7FLb"
        addr = "1Ge1Cn5UzqNnx37bpnoqWEY4McPFGG8Z5f"

        self.do_test(i, wif, None, addr, brain=phrase)
