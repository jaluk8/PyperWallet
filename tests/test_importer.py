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
    Coin = cf.get("btc")

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
        wif_i = importer.WifImporter(self.Coin, prompter.CliPrompter)
        priv_i = importer.PrivImporter(self.Coin, prompter.CliPrompter)
        addr_i = importer.AddrImporter(self.Coin, prompter.CliPrompter)
        pub_i = importer.PubImporter(self.Coin, prompter.CliPrompter)

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        priv = "3C5F262F56AF74A2C314354BE7EA0CCAFEDA1C059E2B5B3B4C3151912C774F\
78"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"
        pub = "02FF136594F723F047A0917A8EC66B56079841AC989FB4F6AC75982FC7F57E9\
80A"

        in1 = [wif]
        in2 = [priv]
        in3 = [addr]
        in4 = [pub]

        self.cli_test(self.do_test, stdin=in1, i=wif_i, w=wif, v=None, a=addr)
        self.cli_test(self.do_test, stdin=in2, i=priv_i, w=wif, v=None, a=addr)
        self.cli_test(self.do_test, stdin=in3, i=addr_i, w=None, v=None,
                      a=addr)
        self.cli_test(self.do_test, stdin=in4, i=pub_i, w=None, v=None, a=addr)


class TestBrainImporter(TestBaseImporter):
    """The same as TestBaseImporter, but for BrainImporter."""

    def test_all(self):
        """Run do_test for a brain phrase."""
        i = importer.BrainImporter(self.Coin)

        phrase = "pyperwalletbrain"
        wif = "KxiDxGBdavV586DaKPAZfA8rB8jpjxXjEhQ6fhSZmZpbhNkX7FLb"
        addr = "1Ge1Cn5UzqNnx37bpnoqWEY4McPFGG8Z5f"

        self.do_test(i, wif, None, addr, brain=phrase)
