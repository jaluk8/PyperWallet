from pyperlib import wallet, prompter, helper, coins, exporter
from unittest import TestCase


class MockPrompter(prompter.BasePrompter):
    """A prompter that returns values based on a dict."""

    answers = {
        "WIF key": "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU",
        "Public address": "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx"}

    @classmethod
    def prompt_info(cls, name, type_f=None, options=None):
        """Check the dict for name and return it."""
        return cls.answers[name]


class TestWalletCli(helper.CliTestCase):
    """Test the wallet's import and export features through cli."""

    stdout = """Coin name: Bitcoin
Compressed: True

Private WIF key: KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU
Private hex key: 3C5F262F56AF74A2C314354BE7EA0CCAFEDA1C059E2B5B3B4C3151912C774\
F78

Public address: 1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx
Public hex key: 02FF136594F723F047A0917A8EC66B56079841AC989FB4F6AC75982FC7F57E\
980A
------
Coin name: Bitcoin
Compressed: False

Private WIF key: 5JGshG5r3noLrhNQYSNNWeBA8uusjMdYoDyMJJvc22MGYDqYYga
Private hex key: 3C5F262F56AF74A2C314354BE7EA0CCAFEDA1C059E2B5B3B4C3151912C774\
F78

Public address: 1FAbaacaMk7zDPU7PLyYQx5zqAhceWkCB1
Public hex key: 04FF136594F723F047A0917A8EC66B56079841AC989FB4F6AC75982FC7F57E\
980A54F713EFFB9ECD9BEADB8CBBADC613E5927B8D786CDD274D194F62D4D20583C0
------
Coin name: Bitcoin
Compressed: True

Public address: 1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx
------
"""

    def do_tests(self):
        """Run various wallet imports."""

        w = wallet.Wallet(Coin="btc", Importer="wif", Exporter="cli",
                          Prompt=MockPrompter)
        w.run()
        print("------")

        w = wallet.Wallet(Coin="btc", Importer="wif", Exporter="cli",
                          Prompt=MockPrompter, compression=False)
        w.run()
        print("------")

        w = wallet.Wallet(Coin="btc", Importer="addr", Exporter="cli",
                          Prompt=MockPrompter)
        w.run()
        print("------")

    def test_cli(self):
        """Run do_tests with stdin and stdout."""
        self.cli_test(self.do_tests, stdout=self.stdout)


class TestWalletGen(TestCase):
    """Test that the Wallet is capable of generating coins."""

    def do_test(self, Coin):
        """Generate one instance of Coin and check for validity."""
        w = wallet.Wallet(Coin=Coin, Importer="gen",
                          Exporter=exporter.BaseExporter)
        exported = w.run()

        coin = Coin(wif=exported.wif)
        self.assertEqual(coin.addr_string(), exported.addr)

    def test_all(self):
        """Run do_test with a variety of coins."""

        cf = coins.CoinFactory()

        for name in ["btc", "eth", "ltc"]:
            Coin = cf.get(name)
            self.do_test(Coin)
