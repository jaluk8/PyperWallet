from pyperlib import coins, data
from pyperlib.coins import bitcoin


class Coin(bitcoin.Coin):
    """A coin that represents the Dash protocol."""

    name = "Dash"
    ticker = "dash"
    wif_version = data.HexData("CC")
    addr_version = data.HexData("4C")
