from pyperlib import data, ec, format, cryptor
from pyperlib.coins.settings import CoinSettings
import importlib
import pkgutil


class InvalidCoinError(Exception):
    """An error that is raised when an address checksum fails."""


class CoinFactory:
    """A class that keeps track of and returns all coin modules."""

    non_coins = ["settings"]

    def __init__(self):
        """Construct the class and search for coin modules."""
        pkgiter = pkgutil.iter_modules(__path__)
        self.coins = []
        for _, name, _ in pkgiter:
            if name not in self.non_coins:
                self.coins.append(name)

    @staticmethod
    def normalize(name):
        """Strip a name of any ambiguous factors."""
        return name.lower().strip(" -_")

    def has(self, name):
        """Return whether a name was found in the modules."""
        return self.normalize(name) in self.coins

    def list(self):
        """Return a list of found module names."""
        return list(self.coins)

    def get(self, name):
        """Return the coin module or None if it doesn't exist."""
        if not self.has(name):
            return None
        p = importlib.import_module('.' + self.normalize(name),
                                    package=__package__)
        return p.Coin


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

    priv_type = data.HexData
    pub_type = data.HexData

    wif_format = format.NoFormat()
    view_format = format.NoFormat()
    addr_format = format.NoFormat()

    def __init__(self, key=None, settings=None, prompt=None):
        """Construct the coin based on spend, view, or address keys."""
        self.keypair = None
        self.wif = None
        self.view = None
        self.addr = None
        self.crypt_type = None

        self.prompt = prompt

        if settings is None:
            self.settings = CoinSettings()
        else:
            self.settings = settings

        self.make_formats()

        if key is None:
            self.gen()
        else:
            ad = format.AutoDetector(self.formats, self.prompt)
            form = ad.detect(key)
            if form is None:
                error_msg = str(key) + " is not recognized as a valid format."
                raise InvalidCoinError(error_msg)

            if form is self.priv_format:
                self.load_priv(self.str2priv(key))
            elif form is self.pub_format:
                self.load_pub(self.str2pub(key))
            elif form is self.wif_format:
                self.from_wif(self.str2wif(key))
            elif form is self.view_format:
                self.from_view(self.str2view(key))
            elif form is self.addr_format:
                self.from_addr(self.str2addr(key))
            elif form.cryptor is not None:
                self.decrypt_format(key, form)
            else:
                msg = form.name + " format is supported but not recognized."
                raise InvalidCoinError(msg)

        self.validate_all()

    def make_formats(self):
        """Create all formats supported by the coin."""
        self.priv_format = format.Format("private key", data.HexData,
                                         length=32)

        pub_u = format.Format("public key", data.HexData, length=33,
                              prefix=["02", "03"])
        pub_c = format.Format("public key", data.HexData, length=65,
                              prefix="04")
        self.pub_format = format.CombinedFormat(pub_u, pub_c)

        self.formats = [self.priv_format, self.wif_format, self.view_format,
                        self.addr_format, self.pub_format]

        for _, crypt in cryptor.CryptorFactory.dict().items():
            self.formats.append(crypt.crypt_format)

    def decrypt_format(self, key, form):
        """Decrypt key, which is encrypted with format form."""
        Cryptor = cryptor.CryptorFactory.get(form.cryptor)
        c = Cryptor(prompt=self.prompt)

        self.wif = form.data_type(key)
        self.crypt_type = form.cryptor

        c.decrypt(self)

    @classmethod
    def str2priv(self, string):
        """Convert ambiguous string to priv_type."""
        if type(string) is not str:
            return string
        return self.priv_type(string)

    @classmethod
    def str2pub(self, string):
        """Convert ambiguous string to pub_type."""
        if type(string) is not str:
            return string
        return self.pub_type(string)

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
        self.calc_all()

    def load_pub(self, pub):
        """Set the keypair from a public key."""
        self.check_curve()
        self.keypair = ec.KeyPair(self.curve, pub=pub)
        self.settings.compression = self.keypair.is_compressed(pub)
        self.calc_all()

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

    def calc_all(self):
        """Attempt to calculate wif/view/addr."""
        if self.keypair is not None:
            if self.keypair.priv is not None:
                self.calc_wif()
                if self.has_privacy:
                    self.calc_view()
            if self.keypair.pub_c is not None:  # true when any pub is present.
                self.calc_addr()

    def wif_string(self):
        """Return wif not as Data but as string."""
        if self.wif is None:
            return None
        return self.wif.export(self.wif_type)

    def view_string(self):
        """Return view not as Data but as string."""
        if self.view is None:
            return None
        return self.view.export(self.view_type)

    def addr_string(self):
        """Return addr not as Data but as string."""
        if self.addr is None:
            return None
        return self.addr.export(self.addr_type)
