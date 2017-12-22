from .. import coins, data
from . import btc


class Coin(btc.Coin):
    """A coin that represents the Bitcoin Cash protocol."""
    name = "Bitcoin Cash"
