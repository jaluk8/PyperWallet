from .. import coins, ec, data, mods

class Coin(coins.BaseCoin):
    """A coin that represents the Bitcoin protocol."""

    name = "Bitcoin"
    curve = ec.SECP256K1

    wif_type = data.Base58Data
    addr_type = data.Base58Data

    wif_version = data.HexData("80")
    addr_version = data.HexData("00")

    def from_wif(self, wif):
        """Generate the coin from wallet import format Data."""
        self.verifybase58check(wif) # TODO: Make this error if it fails.
        priv = wif[1:33] # TODO: Make this set compression flags if x01 is present.
        self.load_priv(priv)

    def from_addr(self, addr):
        """Bitcoin protocol does not support addr->pub conversion."""
        raise NotImplementedError

    def verifybase58check(self, d):
        """Verify that the data has a correct checksum."""
        d2 = self.base58check(d[:-4])
        return d == d2
    
    def base58check(self, d):
        """Return the base58check encoding of Data."""
        check = mods.Sha256(mods.Sha256(d))
        return d + check[:4]

    def wif(self, compressed=True):
        """Return the coin's wallet import format Data."""
        payload = self.wif_version + self.keypair.priv
        if compressed:
            payload += data.HexData("01")
        return self.base58check(payload)
        

    def addr(self, compressed=True):
        """Return the coin's address Data."""
        pub = self.keypair.pub(compressed)
        payload = mods.Ripemd160(mods.Sha256(pub))
        return self.base58check(self.addr_version + payload)
