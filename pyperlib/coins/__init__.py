from pyperlib import data
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
    pass
