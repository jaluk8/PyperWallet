from pyperlib import coins, data
from pyperlib.coins import bitcoin


class Coin(bitcoin.Coin):
    """A coin that represents the Bitcoin Cash protocol."""

    name = "Bitcoin Cash"
    ticker = "bch"
