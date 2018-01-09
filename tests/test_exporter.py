from unittest import TestCase
from pyperlib import exporter, coins, helper


class TestExporterFactory(helper.TestNameFactory):
    """Test the ExporterFactory's get method."""

    factory = exporter.ExporterFactory

    def test_all(self):
        """Attempt to export various names."""
        self.do_test("Base", None)
        self.do_test("Nonexistant", None)
        self.do_test("cli", exporter.CliExporter)


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


class TestCliExporter(TestBaseExporter, helper.CliTestCase):
    """Same as TestBaseExporter, but for the Cli exporter."""

    maxDiff = None
    out1 = """Coin name: Bitcoin
Compressed: True

Private WIF key: KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU
Private hex key: 3C5F262F56AF74A2C314354BE7EA0CCAFEDA1C059E2B5B3B4C3151912C774\
F78

Public address: 1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx
Public hex key: 02FF136594F723F047A0917A8EC66B56079841AC989FB4F6AC75982FC7F57E\
980A
"""

    out2 = """Coin name: Bitcoin
Compressed: True

Public address: 1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx
"""

    def make_test(self, e, c):
        """Return a function that tests exporting on Coin c with e."""
        def test():
            """The test function for use in cli_test."""
            e.run(c)
        return test

    def test_all(self):
        """Run do_test with all test sets."""
        e = exporter.CliExporter()

        wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
        addr = "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"

        self.cli_test(self.make_test(e, self.Coin(wif=wif)), stdout=self.out1)
        self.cli_test(self.make_test(e, self.Coin(addr=addr)),
                      stdout=self.out2)
