from .. import coins, data
from . import btc

class Coin(btc.Coin):
    """A coin that represents the Feathercoin protocol."""

    wif_version = data.HexData("8E")
    addr_version = data.HexData("0E")
