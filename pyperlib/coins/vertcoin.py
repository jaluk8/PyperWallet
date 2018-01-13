from pyperlib import coins, data
from pyperlib.coins import bitcoin


class Coin(bitcoin.Coin):
    """A coin that represents the Vertcoin protocol."""

    name = "Vertcoin"
    ticker = "vtc"
    wif_version = data.HexData("80")
    addr_version = data.HexData("47")
