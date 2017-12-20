from pyperlib import data, ec
import importlib
import pkgutil

class CoinList:
    def __init__(self):
        pkgiter = pkgutil.iter_modules(__path__)
        self.coins = []
        for _, name, _ in pkgiter:
            self.coins.append(name)

    def has_coin(self, name):
        return name in self.coins

    def list_coins(self):
        return list(self.coins)

    def get_coin(self, name):
        try:
            p = importlib.import_module('.btc', package=__package__)
        except ImportError:
            return None
        return p.Coin

class BaseCoin:
    curve = None
    has_privacy = False

    def __init__(self, wif=None, view=None, addr=None):
        self.keypair = None
        if wif is not None:
            self.from_wif(wif)
        elif view is not None:
            self.from_view(view)
        elif addr is not None:
            self.from_addr(addr)
        else:
            self.gen()

    def check_curve(self):
        if self.curve is None:
            raise NotImplementedError
    
    def gen(self):
        self.check_curve()
        self.keypair = ec.KeyPair(self.curve)

    def load_priv(self, priv):
        self.check_curve()
        self.keypair = ec.KeyPair(self.curve, priv=priv)

    def load_pub(self, pub):
        self.check_curve()
        self.keypair = ec.KeyPair(self.curve, pub=pub)

    def from_wif(self, wif):
        raise NotImplementedError

    def from_view(self, view):
        raise NotImplementedError
    
    def from_addr(self, addr):
        raise NotImplementedError

    def wif(self, compressed=True):
        raise NotImplementedError

    def view(self, compressed=True):
        raise NotImplementedError

    def addr(self, compressed=True):
        raise NotImplementedError
