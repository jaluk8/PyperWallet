from unittest import TestCase
from pyperlib import importer, coins, coinutil, prompter, helper
from pyperlib.coins.basecoin import Coin as BaseCoin


class TestImporterFactory(helper.TestNameFactory):
    """Test the ImporterFactory's get method."""

    factory = importer.ImporterFactory

    def test_all(self):
        """Attempt to import various names."""
        self.do_test("base", None)
        self.do_test("nonexistant", None)
        self.do_test("prompt", importer.PromptImporter)


class TestBaseImporter(TestCase):
    """A TestCase that creates BaseImporters and verifies their output."""

    cf = coinutil.CoinFactory
    Coin = cf.get("bitcoin")

    def do_test(self, i, w, v, a, *args, **kwargs):
        """Uses importer i with given args, checking that the results fit."""
        coin = i.run(*args, **kwargs)
        self.assertIsInstance(coin, BaseCoin)

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

        self.do_test(i, wif, None, addr, key=wif)
        self.do_test(i, None, None, addr, key=addr)


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
        i = importer.PromptImporter(self.Coin, prompter.CliPrompter())

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        priv = "3C5F262F56AF74A2C314354BE7EA0CCAFEDA1C059E2B5B3B4C3151912C774F\
78"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        in1 = [wif]
        in2 = [priv]
        in3 = [addr]

        self.cli_test(self.do_test, stdin=in1, i=i, w=wif, v=None, a=addr)
        self.cli_test(self.do_test, stdin=in2, i=i, w=wif, v=None, a=addr)
        self.cli_test(self.do_test, stdin=in3, i=i, w=None, v=None, a=addr)


class TestBrainImporter(TestBaseImporter):
    """The same as TestBaseImporter, but for BrainImporter."""

    def test_all(self):
        """Run do_test for a brain phrase."""
        i = importer.BrainImporter(self.Coin)

        phrase = "pyperwalletbrain"
        wif = "KxiDxGBdavV586DaKPAZfA8rB8jpjxXjEhQ6fhSZmZpbhNkX7FLb"
        addr = "1Ge1Cn5UzqNnx37bpnoqWEY4McPFGG8Z5f"

        self.do_test(i, wif, None, addr, brain=phrase)
