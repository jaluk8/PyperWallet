from pyperlib import coins, data
from pyperlib.coins import bitcoin


class Coin(bitcoin.Coin):
    """A coin that represents the Feathercoin protocol."""

    name = "Feathercoin"
    ticker = "ftc"
    wif_version = data.HexData("8E")
    addr_version = data.HexData("0E")
