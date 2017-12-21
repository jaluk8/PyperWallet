from .. import coins, data
from . import btc

class Coin(btc.Coin):
    """A coin that represents the Dash protocol."""

    wif_version = data.HexData("CC")
    addr_version = data.HexData("4C")
