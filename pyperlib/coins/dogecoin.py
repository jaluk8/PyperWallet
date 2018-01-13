from pyperlib import coins, data
from pyperlib.coins import bitcoin


class Coin(bitcoin.Coin):
    """A coin that represents the Dogecoin protocol."""

    name = "Dogecoin"
    ticker = "doge"
    wif_version = data.HexData("9E")
    addr_version = data.HexData("1E")
