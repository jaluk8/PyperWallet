from pyperlib import data, mods, helper


class ImporterFactory(helper.NameFactory):
    """A class that makes importers from names."""

    suffix = "Importer"
    pool = globals()


class BaseImporter:
    """An importer that imports using args, rather than external sources."""

    description = "no description"

    def __init__(self, Coin, prompt=None):
        """Initializes the importer with a Coin class."""
        self.Coin = Coin
        self.prompt = prompt

    def run(self, **kwargs):
        """Returns the result of creating a Coin with kwargs."""
        return self.Coin(**kwargs)


class GenImporter(BaseImporter):
    """An importer that takes no arguments and just generates coins."""

    description = "generate a new coin using random numbers"

    def run(self):
        """Returns the result of creating a Coin from generation."""
        return super().run()


class WifImporter(BaseImporter):
    """An importer that imports using a wif string."""

    description = "import the coin from a wallet import format key"

    def run(self, wif=None):
        """Return the result of creating a Coin from wif."""
        if wif is None:
            wif = self.prompt.prompt_info(name="WIF key", type_f=str)
        return super().run(wif=wif)


class PrivImporter(BaseImporter):
    """An importer that imports using a private key."""

    description = "import the coin from a hexadecimal private key"

    def run(self, priv=None):
        """Return the result of creating a Coin from priv."""
        if priv is None:
            priv = self.prompt.prompt_info(name="Private key", type_f=str)
        return super().run(priv=priv)


class PubImporter(BaseImporter):
    """An importer that imports using a public key."""

    description = "import the coin from a hexadecimal public key (no private \
key)"

    def run(self, pub=None):
        """Return the result of creating a Coin from pub."""
        if pub is None:
            pub = self.prompt.prompt_info(name="Public key", type_f=str)
        return super().run(pub=pub)


class AddrImporter(BaseImporter):
    """An importer that imports using a addr string."""

    description = "import the coin from an address (no private key)"

    def run(self, addr=None):
        """Return the result of creating a Coin from addr."""
        if addr is None:
            addr = self.prompt.prompt_info(name="Public address", type_f=str)
        return super().run(addr=addr)


class BrainImporter(BaseImporter):
    """An importer for brainwallets using sha256."""

    description = "import the coin using a memorized 'brain wallet' phrase"

    def run(self, brain=None):
        """Uses brainwallet string given to make a private key."""
        if brain is None:
            brain = self.prompt.prompt_pass(name="Brain phrase", type_f=str)

        brain_data = data.StringData(brain)
        priv = mods.Sha256(brain_data)
        return super().run(priv=priv)
