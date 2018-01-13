from pyperlib import coins, data
from pyperlib.coins import btc


class Coin(btc.Coin):
    """A coin that represents the Vertcoin protocol."""

    name = "Vertcoin"
    wif_version = data.HexData("80")
    addr_version = data.HexData("47")
