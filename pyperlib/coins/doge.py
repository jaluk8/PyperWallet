from .. import coins, data
from . import btc

class Coin(btc.Coin):
    """A coin that represents the Dogecoin protocol."""

    wif_version = data.HexData("9E")
    addr_version = data.HexData("1E")
