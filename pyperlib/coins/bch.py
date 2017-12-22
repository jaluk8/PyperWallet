from pyperlib import coins, data
from pyperlib.coins import btc


class Coin(btc.Coin):
    """A coin that represents the Bitcoin Cash protocol."""
    name = "Bitcoin Cash"
