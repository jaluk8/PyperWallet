from pyperlib import coins, ec, data, mods


class Coin(coins.BaseCoin):
    """A coin that represents the Bitcoin protocol."""

    name = "Bitcoin"
    curve = ec.SECP256K1

    wif_type = data.Base58Data
    addr_type = data.Base58Data

    has_priv_csum = True
    has_addr_csum = True

    wif_version = data.HexData("80")
    addr_version = data.HexData("00")

    def from_wif(self, wif):
        """Create the coin from wallet import format Data."""
        self.verifybase58check(wif)

        if len(wif) == 38:
            self.settings.compression = True
        elif len(wif) == 37:
            self.settings.compression = False
        priv = wif[1:33]
        self.load_priv(priv)

    def from_addr(self, addr):
        """Create a coin object only containing the addr."""
        self.verifybase58check(addr)
        self.addr = addr

    def verifybase58check(self, d):
        """Verify that the data has a correct checksum."""
        d2 = self.base58check(d[:-4])
        if not d == d2:
            raise coins.InvalidCoinError("Base58 Checksum failed.")

    def base58check(self, d):
        """Return the base58check encoding of Data."""
        check = mods.Sha256(mods.Sha256(d))
        return d + check[:4]

    def validate_wif(self):
        """Raise an error if the wif checksum fails."""
        self.verifybase58check(self.wif)

    def validate_addr(self):
        """Raise an error if the addr checksum fails."""
        self.verifybase58check(self.addr)

    def calc_wif(self):
        """Calculate the wif key from the keypair."""
        payload = self.wif_version + self.keypair.priv
        if self.settings.compression:
            payload += data.HexData("01")
        self.wif = self.base58check(payload)

    def calc_addr(self):
        """Calculate the addr from the keypair."""
        pub = self.keypair.pub(self.settings.compression)
        payload = mods.Ripemd160(mods.Sha256(pub))
        self.addr = self.base58check(self.addr_version + payload)
