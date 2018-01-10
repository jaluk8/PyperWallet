from unittest import TestCase
from pyperlib import cryptor, coins, helper


class TestCryptorFactory(helper.TestNameFactory):
    """Test the CryptorFactory's get method."""

    factory = cryptor.CryptorFactory

    def test_all(self):
        """Attempt to import various names."""
        self.do_test("Base", None)
        self.do_test("Nonexistant", None)


class TestBaseCryptor(TestCase):
    """Encrypt and decrypt a coin, checking for correctness."""

    cf = coins.CoinFactory()
    Coin = cf.get_coin("btc")
    wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"

    enc_wif = "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU"
    cryptor = cryptor.BaseCryptor()

    def do_test(self, **kwargs):
        """Encrypt and decrypt one coin with the given args."""

        coin = self.make_coin()
        wif = coin.wif

        self.cryptor.encrypt(coin, **kwargs)
        self.assertEqual(coin.crypt_type, self.cryptor.name)
        self.assertEqual(coin.wif_string(), self.enc_wif)

        self.cryptor.decrypt(coin, **kwargs)
        self.assertEqual(coin.crypt_type, None)
        self.assertEqual(coin.wif, wif)

    def make_coin(self):
        """Generate the coin from self.wif."""

        coin = self.Coin(wif=self.wif)
        return coin

    def test_all(self):
        """Run do_test (no arguments needed for BaseCryptor)."""
        self.do_test()


class TestBIP38Cryptor(TestBaseCryptor):
    """Encrypt and decrypt a coin, with bip38."""

    cryptor = cryptor.BIP38Cryptor()
    enc_wif = "6PYS3EufMDqJZMqKxHZ2fGTe1FDGWQy9vYrnuJeiUUxppqTDfUNKoVjJXu"

    def test_all(self):
        """Run do_test with various passwords."""
        self.do_test(passphrase="12345")
