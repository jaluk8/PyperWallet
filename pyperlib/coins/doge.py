from pyperlib import coins, data
from pyperlib.coins import btc


class Coin(btc.Coin):
    """A coin that represents the Dogecoin protocol."""

    name = "Dogecoin"
    wif_version = data.HexData("9E")
    addr_version = data.HexData("1E")
