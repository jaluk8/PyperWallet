from pyperlib import coins, data
from pyperlib.coins import bitcoin


class Coin(bitcoin.Coin):
    """A coin that represents the Litecoin protocol."""

    name = "Litecoin"
    ticker = "ltc"
    wif_version = data.HexData("B0")
    addr_version = data.HexData("30")
