from .. import coins, data
from . import btc

class Coin(btc.Coin):
    """A coin that represents the Litecoin protocol."""

    name = "Litecoin"
    wif_version = data.HexData("B0")
    addr_version = data.HexData("30")
