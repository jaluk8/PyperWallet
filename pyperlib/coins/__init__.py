from pyperlib import data, ec
import importlib
import pkgutil


class InvalidCoinError(Exception):
    """An error that is raised when an address checksum fails."""


class CryptError(Exception):
    """An error that is raised when there is an issue with cryptography."""


class CoinList:
    """A class that keeps track of and returns all coin modules."""

    def __init__(self):
        """Construct the class and search for coin modules."""
        pkgiter = pkgutil.iter_modules(__path__)
        self.coins = []
        for _, name, _ in pkgiter:
            self.coins.append(name)

    def has_coin(self, name):
        """Return whether a name was found in the modules."""
        return name in self.coins

    def list_coins(self):
        """Return a list of found module names."""
        return list(self.coins)

    def get_coin(self, name):
        """Return the coin module or None if it doesn't exist."""
        if not self.has_coin(name):
            return None
        p = importlib.import_module('.' + name, package=__package__)
        return p.Coin


class CoinSettings:
    """A container for keeping track of user-defined coin settings."""
    compression = True
    cryptor = None


class BaseCoin:
    """The base class for all coins."""

    name = "[Base Coin]"
    curve = None
    has_privacy = False

    has_priv_csum = False
    has_view_csum = False
    has_addr_csum = False

    wif_type = None
    view_type = None
    addr_type = None

    def __init__(self, wif=None, view=None, addr=None):
        """Construct the coin based on spend, view, or address keys."""
        self.keypair = None
        self.wif = None
        self.view = None
        self.addr = None
        self.crypt_type = None

        self.settings = CoinSettings()

        if wif is not None:
            self.from_wif(self.str2wif(wif))
        elif view is not None:
            self.from_view(self.str2view(view))
        elif addr is not None:
            self.from_addr(self.str2addr(addr))
        else:
            self.gen()

        self.validate_all()

    @classmethod
    def str2wif(self, string):
        """Convert ambiguous string to wif_type."""
        if type(string) is not str:
            return string
        if self.wif_type is None:
            raise NotImplementedError(self.name + " does not support str2wif.")
        else:
            return self.wif_type(string)

    @classmethod
    def str2view(self, string):
        """Convert ambiguous string to view_type."""
        if type(string) is not str:
            return string
        if self.view_type is None:
            raise NotImplementedError(
                self.name + " does not support str2view.")
        else:
            return self.view_type(string)

    @classmethod
    def str2addr(self, string):
        """Convert ambiguous string to addr_type."""
        if type(string) is not str:
            return string
        if self.addr_type is None:
            raise NotImplementedError(
                self.name + " does not support str2addr.")
        else:
            return self.addr_type(string)

    def check_curve(self):
        """Raise an error if the curve is not implemented."""
        if self.curve is None:
            raise NotImplementedError(self.name + " does not support ec.")

    def validate_wif(self):
        """Raise an error if the wif checksum fails."""

    def validate_view(self):
        """Raise an error if the view checksum fails."""

    def validate_addr(self):
        """Raise an error if the addr checksum fails."""

    def validate_all(self):
        """Attempt to validate all available information."""
        if self.wif is not None:
            self.validate_wif()
        if self.has_privacy and self.view is not None:
            self.validate_view()
        if self.addr is not None:
            self.validate_addr()

    def gen(self):
        """Generate the coin from its curve."""
        self.check_curve()
        self.keypair = ec.KeyPair(self.curve)
        self.calc_wif()
        if self.has_privacy:
            self.calc_view()
        self.calc_addr()

    def load_priv(self, priv):
        """Set the keypair from a private key."""
        self.check_curve()
        self.keypair = ec.KeyPair(self.curve, priv=priv)

    def load_pub(self, pub):
        """Set the keypair from a public key."""
        self.check_curve()
        self.keypair = ec.KeyPair(self.curve, pub=pub)

    def from_wif(self, wif):
        """Generate the coin from wallet import format Data."""
        raise NotImplementedError(self.name + " does not support from_wif.")

    def from_view(self, view):
        """Generate the coin from viewkey Data."""
        raise NotImplementedError(self.name + " does not support from_view.")

    def from_addr(self, addr):
        """Generate the coin from address Data."""
        raise NotImplementedError(self.name + " does not support from_addr.")

    def calc_wif(self):
        """Calculate the wif key from the keypair."""
        raise NotImplementedError(self.name + " does not support wif.")

    def calc_view(self):
        """Calculate the view key from the keypair."""
        raise NotImplementedError(self.name + " does not support view.")

    def calc_addr(self):
        """Calculate the addr from the keypair."""
        raise NotImplementedError(self.name + " does not support addr.")

    def wif_string(self):
        """Return wif not as Data but as string."""
        return self.wif.export(self.wif_type)

    def view_string(self):
        """Return view not as Data but as string."""
        return self.view.export(self.view_type)

    def addr_string(self):
        """Return addr not as Data but as string."""
        return self.addr.export(self.addr_type)

    def encrypt(self, **kwargs):
        """Changes the unencrypted wif into an encrypted one."""
        if self.crypt_type is not None:
            raise CryptError("Coin is already encrypted.")
        elif self.settings.cryptor is None:
            raise CryptError("No cryptor is selected.")

        self.wif = self.settings.cryptor.encrypt(wif=self.wif, **kwargs)
        self.crypt_type = self.settings.cryptor.name

    def decrypt(self, **kwargs):
        """Changes the encrypted wif key to a decrypted one."""
        if self.crypt_type is None:
            raise CryptError("Coin is not encrypted.")
        elif self.settings.cryptor is None:
            raise CryptError("No cryptor is selected.")
        elif self.crypt_type != self.settings.cryptor.name:
            raise CryptError("Cryptor does not match the encryption type.")

        self.wif = self.settings.cryptor.decrypt(wif=self.wif, **kwargs)
        self.crypt_type = None
