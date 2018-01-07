from pyperlib import coins, ec, data, mods


class Coin(coins.BaseCoin):
    """A coin that represents the Ethereum protocol."""

    name = "Ethereum"
    curve = ec.SECP256K1

    has_addr_csum = True

    wif_type = data.StringData
    addr_type = data.StringData

    def from_wif(self, wif):
        """Create the coin from wallet import format Data."""
        priv = data.HexData(wif.string)
        self.load_priv(priv)

    def from_addr(self, addr):
        """Create a coin containing only the addr."""
        self.eth_checksum(addr)
        self.addr = addr

    def eth_checksum(self, addr):
        """Converts a lowercase string address into a checksummed one."""
        addr_str = addr.string.lower()[2:]
        csum = mods.Keccak(data.StringData(addr_str)).hex
        out = "0x"

        for a, c in zip(addr_str, csum):
            if c in "89ABCDEF":
                out += a.upper()
            else:
                out += a

        return data.StringData(out)

    def validate_addr(self):
        """Raise an error if the addr checksum fails."""
        if self.addr != self.eth_checksum(self.addr):
            raise coins.InvalidCoinError

    def calc_wif(self):
        """Calculate the wif key from the keypair."""
        wif_hex = self.keypair.priv.hex.lower()
        self.wif = data.StringData(wif_hex)

    def calc_addr(self):
        """Calculate the addr from the keypair."""
        keccak = mods.Keccak(self.keypair.pub_u[1:])
        addr_hex = keccak[-20:]
        addr_str = "0x" + addr_hex.hex
        addr = data.StringData(addr_str)
        self.addr = self.eth_checksum(addr)
