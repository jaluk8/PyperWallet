from pyperlib import mods, helper, data


class CryptorFactory(helper.NameFactory):
    """A class that makes cryptors from names."""
    suffix = "Cryptor"
    pool = globals()


class BaseCryptor:
    """The base class for all encrypting/decrypting objects."""

    name = "identity"

    def __init__(self):
        """Cryptors require no initialization right now."""

    def encrypt(self, coin, **kwargs):
        """Return the wif encrypted with no encryption."""

    def decrypt(self, coin, **kwargs):
        """Return the encrypted wif as an unencrypted type."""


class BIP38Cryptor(BaseCryptor):
    """Encrypt/decrypt using the BIP 38 standard."""

    name = "bip38"

    def encrypt(self, coin, passphrase):
        """Return the wif encrypted with bip38."""
        prefix = data.HexData("0142")
        if coin.settings.compression:
            flag = data.HexData("E0")
        else:
            flag = data.HexData("C0")

        addr_string = data.StringData(coin.addr_string())
        addr_hash = mods.Sha256(mods.Sha256(addr_string))[:4]

        passphrase = data.StringData(passphrase)
        key = mods.Scrypt(passphrase, addr_hash)

        key_h1 = key[:32]
        key_h2 = key[32:]

        block1 = mods.Xor(coin.keypair.priv[:16], key_h1[:16])
        block2 = mods.Xor(coin.keypair.priv[16:], key_h1[16:])

        enc_h1 = mods.Aes256Enc(block1, key_h2)
        enc_h2 = mods.Aes256Enc(block2, key_h2)

        enc_wif = prefix + flag + addr_hash + enc_h1 + enc_h2
        coin.wif = coin.base58check(enc_wif)

    def decrypt(self, coin, passphrase):
        """Return the encrypted wif as bip38."""
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

        coin.load_priv(priv_h1 + priv_h2)
