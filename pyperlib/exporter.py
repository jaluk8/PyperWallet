from copy import deepcopy
from pyperlib import helper
import sys


class ExporterFactory(helper.NameFactory):
    """A class that makes exporters from names."""
    suffix = "Exporter"
    pool = globals()


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
        self.compression = coin.get_settings().compression
        self.crypt_type = coin.crypt_type

        if coin.keypair is not None:
            if coin.keypair.priv is not None:
                self.priv = coin.keypair.priv.hex
            if coin.keypair.pub_u is not None:
                self.pub = coin.keypair.pub(self.compression).hex


class BaseExporter:
    """Take in a Coin object and export it to python values."""

    description = "no description"

    def __init__(self, f=None):
        """Create the exporter given an output file."""
        if f is None:
            self.out_file = sys.stdout
        else:
            self.out_file = f

    def run(self, c):
        """Exports the given coin to an Exported class."""
        return Exported(c)


class TextExporter(BaseExporter):
    """Take in a Coin object and print its data as text."""

    description = "print all known data of the coin to the command line"

    def print2file(self, *args):
        """Print the arguments to self.file."""
        print(*args, file=self.out_file)

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
                    self.print2file("")
                    blank = True
            elif value is None:
                pass
            else:
                self.print2file(title + ": " + str(value))
                blank = False
