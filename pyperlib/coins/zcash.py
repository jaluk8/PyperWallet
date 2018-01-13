from pyperlib import coins, data
from pyperlib.coins import bitcoin


class Coin(bitcoin.Coin):
    """A coin that represents the ZCash protocol."""

    name = "ZCash"
    ticker = "zec"
    wif_version = data.HexData("80")
    addr_version = data.HexData("1CB8")
