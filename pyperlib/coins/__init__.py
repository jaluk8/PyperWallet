from pyperlib import data, ec
import importlib
import pkgutil

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

class BaseCoin:
    """The base class for all coins."""

    curve = None
    has_privacy = False
    load_from_addr = False

    wif_type = None
    view_type = None
    addr_type = None

    def __init__(self, wif=None, view=None, addr=None):
        """Construct the coin based on spend, view, or address keys."""
        self.keypair = None
        if wif is not None:
            self.from_wif(wif)
        elif view is not None:
            self.from_view(view)
        elif addr is not None:
            self.from_addr(addr)
        else:
            self.gen()

    @classmethod
    def str2wif(self, string):
        """Convert ambiguous string to wif_type."""
        if self.wif_type is None:
            raise NotImplementedError
        else:
            return self.wif_type(string)

    @classmethod
    def str2view(self, string):
        """Convert ambiguous string to view_type."""
        if self.view_type is None:
            raise NotImplementedError
        else:
            return self.view_type(string)

    @classmethod
    def str2addr(self, string):
        """Convert ambiguous string to addr_type."""
        if self.addr_type is None:
            raise NotImplementedError
        else:
            return self.addr_type(string)

    def check_curve(self):
        """Raise an error if the curve is not implemented."""
        if self.curve is None:
            raise NotImplementedError
    
    def gen(self):
        """Generate the coin from its curve."""
        self.check_curve()
        self.keypair = ec.KeyPair(self.curve)

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
        raise NotImplementedError

    def from_view(self, view):
        """Generate the coin from viewkey Data."""
        raise NotImplementedError
    
    def from_addr(self, addr):
        """Generate the coin from address Data."""
        raise NotImplementedError

    def wif(self, compressed=True):
        """Return the coin's wallet import format Data."""
        raise NotImplementedError

    def view(self, compressed=True):
        """Return the coin's viewkey Data."""
        raise NotImplementedError

    def addr(self, compressed=True):
        """Return the coin's address Data."""
        raise NotImplementedError
