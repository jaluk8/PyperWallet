from copy import deepcopy


class Exported:
    """A container for raw exported data."""

    name = None
    compression = None

    crypt_type = None
    wif = None
    priv = None

    addr = None
    pub = None

    def __init__(self, coin):
        """Extracts all information from a coin."""

        self.name = coin.name
        self.wif = coin.wif_string()  # TODO: Add view key
        self.addr = coin.addr_string()
        self.compression = coin.settings.compression
        self.crypt_type = coin.crypt_type

        if coin.keypair is not None:
            if coin.keypair.priv is not None:
                self.priv = coin.keypair.priv.hex
            if coin.keypair.pub_u is not None:
                self.pub = coin.keypair.pub(self.compression).hex


class BaseExporter:
    """Takes in a Coin object and exports it to python values."""

    def __init__(self):
        """Exporters require no initialization."""
        pass

    def run(self, c):
        """Exports the given coin to an Exported class."""
        return Exported(c)


class CliExporter(BaseExporter):
    """Takes in a Coin object and prints its data to stdout."""

    def run(self, c):
        """Exports the given coin to stdout."""

        e = Exported(c)
        elements = [
            ("Coin name", e.name),
            ("Compressed", e.compression),
            (None, None),
            ("WIF encryption", e.crypt_type),
            ("Private WIF key", e.wif),
            ("Private hex key", e.priv),
            (None, None),
            ("Public address", e.addr),
            ("Public hex key", e.pub)]

        blank = True
        for title, value in elements:
            if title is None:
                if not blank:
                    print("")
                    blank = True
            elif value is None:
                pass
            else:
                print(title + ": " + str(value))
                blank = False
