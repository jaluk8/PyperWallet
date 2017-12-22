from .. import coins, data
from . import btc


class Coin(btc.Coin):
    """A coin that represents the ZCash protocol."""

    name = "ZCash"
    wif_version = data.HexData("80")
    addr_version = data.HexData("1CB8")
