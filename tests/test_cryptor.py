from unittest import TestCase
from pyperlib import cryptor, coins


class TestBaseCryptor(TestCase):
    """Encrypt and decrypt a coin, checking for correctness."""

    cl = coins.CoinList()
    wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"

    enc_wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
    cryptor = cryptor.BaseCryptor()

    def do_test(self, **kwargs):
        """Encrypt and decrypt one coin with the given args."""

        coin = self.make_coin()
        wif = coin.wif

        coin.encrypt(**kwargs)
        self.assertEqual(coin.crypt_type, coin.settings.cryptor.name)
        self.assertEqual(coin.wif_string(), self.enc_wif)

        coin.decrypt(**kwargs)
        self.assertEqual(coin.crypt_type, None)
        self.assertEqual(coin.wif, wif)

    def make_coin(self):
        """Generate the coin from self.wif."""

        Coin = self.cl.get_coin("btc")
        coin = Coin(wif=self.wif)
        coin.settings.cryptor = self.cryptor
        return coin

    def test_all(self):
        """Run do_test (no arguments needed for BaseCryptor)."""
        self.do_test()
