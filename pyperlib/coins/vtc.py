from .. import coins, data
from . import btc


class Coin(btc.Coin):
    """A coin that represents the Vertcoin protocol."""

    name = "Vertcoin"
    wif_version = data.HexData("C7")
    addr_version = data.HexData("47")
