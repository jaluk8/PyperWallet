from pyperlib import mods


class BaseCryptor:
    """The base class for all encrypting/decrypting objects."""

    name = "identity"

    def __init__(self):
        """Cryptors require no initialization right now."""

    def encrypt(self, wif=None, **kwargs):
        """Return the wif encrypted with no encryption."""
        return wif

    def decrypt(self, wif=None, **kwargs):
        """Return the encrypted wif as an unencrypted type."""
        return wif
