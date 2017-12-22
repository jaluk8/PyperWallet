from pyperlib import coins, data
from pyperlib.coins import btc


class Coin(btc.Coin):
    """A coin that represents the Feathercoin protocol."""

    name = "Feathercoin"
    wif_version = data.HexData("8E")
    addr_version = data.HexData("0E")
