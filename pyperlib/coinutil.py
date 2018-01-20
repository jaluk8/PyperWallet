from pyperlib import helper
import pkgutil
import importlib


class CoinFinder:
    """Find coin classes in the pyperlib.coins package."""

    @staticmethod
    def normalize(name):
        """Normalize a name into a purely alphanumeric name."""
        return ''.join(c for c in name.lower() if c.isalnum())

    @classmethod
    def Coin2dict(cls, Coin):
        """Return a dictionary entry for a Coin class."""
        name = cls.normalize(Coin.name)
        return {name: Coin}

    @classmethod
    def get_coin_path(cls):
        """Find the path of the coins package."""
        assert __file__[-11:] == "coinutil.py"
        path = __file__[:-7]  # The path up to .../pyperlib/coin
        path += "s"
        return [path]

    @classmethod
    def pool(cls):
        """Return a pool containing all Coin classes."""
        pool = {}

        pkgiter = pkgutil.iter_modules(cls.get_coin_path())

        for _, name, _ in pkgiter:
            pkg = importlib.import_module("pyperlib.coins." + name)

            try:
                d = cls.Coin2dict(pkg.Coin)
                pool.update(d)
            except AttributeError:
                pass  # No Coin class

            try:
                for Coin in pkg.CoinList.list():
                    d = cls.Coin2dict(Coin)
                    pool.update(d)
            except AttributeError:
                pass  # No CoinList class

        return pool


class CoinFactory(helper.NameFactory):
    """A factory to get coin classes from names."""

    suffix = ""
    caps = False
    pool = None

    @classmethod
    def init(cls):
        """Initialize the pool by finding all coins."""
        cls.pool = CoinFinder.pool()
