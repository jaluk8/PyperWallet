from pyperlib import mods, helper, data
from copy import deepcopy


class DecryptionUnsucessfulError(Exception):
    """Raised when a password is wrong or decryption fails otherwise."""


class CryptorError(Exception):
    """An error that is raised when cryptor types are wrong."""


class CryptorFactory(helper.NameFactory):
    """A class that makes cryptors from names."""
    suffix = "Cryptor"
    pool = globals()


class BaseCryptor:
    """The base class for all encrypting/decrypting objects."""

    name = "identity"
    description = "no description"

    def __init__(self, prompt=None):
        """Create a cryptor with a prompter for getting passwords."""
        self.prompt = prompt

    def run_encrypt(self, coin):
        """Encrypt with nothing."""

    def run_decrypt(self, coin):
        """Decrypt with nothing."""

    def encrypt(self, coin, **kwargs):
        """Changes the unencrypted wif into an encrypted one."""
        if coin.crypt_type is not None:
            raise CryptorError("Coin is already encrypted.")

        self.run_encrypt(coin, **kwargs)

        coin.keypair = None
        coin.crypt_type = self.name

    def decrypt(self, coin, **kwargs):
        """Changes the encrypted wif key to a decrypted one."""
        if coin.crypt_type is None:
            raise CryptorError("Coin is not encrypted.")
        elif coin.crypt_type != self.name:
            raise CryptorError("Cryptor does not match the encryption type.")

        self.run_decrypt(coin, **kwargs)

        coin.validate_all()
        coin.crypt_type = None


class Bip38Cryptor(BaseCryptor):
    """Encrypt/decrypt using the BIP 38 standard."""

    name = "bip38"
    description = "an early bitcoin encryption standard (keys start with 6P)"

    def base58check(self, d):
        """Return the base58checksum of the given data."""
        return mods.Sha256(mods.Sha256(d))[:4]

    def addr_hash(self, coin):
        """Compute a BIP38 address hash from the coin's addr."""
        addr_string = data.StringData(coin.addr_string())
        return self.base58check(addr_string)

    def run_encrypt(self, coin, passphrase=None):
        """Encrypt with bip38, mutating coin.wif."""
        if passphrase is None:
            passphrase = self.prompt.prompt_pass("BIP38 Password")

        prefix = data.HexData("0142")
        if coin.settings.compression:
            flag = data.HexData("E0")
        else:
            flag = data.HexData("C0")

        addr_hash = self.addr_hash(coin)

        passphrase = data.StringData(passphrase)
        key = mods.Scrypt(passphrase, addr_hash)

        key_h1 = key[:32]
        key_h2 = key[32:]

        block1 = mods.Xor(coin.keypair.priv[:16], key_h1[:16])
        block2 = mods.Xor(coin.keypair.priv[16:], key_h1[16:])

        enc_h1 = mods.Aes256Enc(block1, key_h2)
        enc_h2 = mods.Aes256Enc(block2, key_h2)

        enc_wif = prefix + flag + addr_hash + enc_h1 + enc_h2
        coin.wif = enc_wif + self.base58check(enc_wif)

    def run_decrypt(self, coin, passphrase=None):
        """Decrypt with bip38, loading the new private key."""
        if passphrase is None:
            passphrase = self.prompt.prompt_pass("BIP38 Password",
                                                 repeat=False)

        flag = coin.wif[2]
        if flag.hex == "E0":
            compression = True
        elif flag.hex == "C0":
            compression = False
        else:
            raise DecryptionUnsucessfulError("Invalid bip38 wif key flag")

        addr_hash = coin.wif[3:7]

        passphrase = data.StringData(passphrase)
        key = mods.Scrypt(passphrase, addr_hash)

        key_h1 = key[:32]
        key_h2 = key[32:]

        enc_h1 = coin.wif[7:23]
        enc_h2 = coin.wif[23:39]

        block1 = mods.Aes256Dec(enc_h1, key_h2)
        block2 = mods.Aes256Dec(enc_h2, key_h2)

        priv_h1 = mods.Xor(block1, key_h1[:16])
        priv_h2 = mods.Xor(block2, key_h1[16:])

        priv = priv_h1 + priv_h2

        coin_test = deepcopy(coin)
        coin_test.load_priv(priv)
        addr_hash2 = self.addr_hash(coin_test)

        if addr_hash == addr_hash2:
            coin.load_priv(priv)
            coin.settings.compression = compression
        else:
            raise DecryptionUnsucessfulError("Password incorrect")
