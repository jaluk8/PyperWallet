from pyperlib import data, mods, helper


class ImporterFactory(helper.NameFactory):
    """A class that makes importers from names."""

    suffix = "Importer"
    pool = globals()


class BaseImporter:
    """An importer that imports using args, rather than external sources."""

    def __init__(self, Coin, prompt=None):
        """Initializes the importer with a Coin class."""
        self.Coin = Coin
        self.prompt = prompt

    def run(self, **kwargs):
        """Returns the result of creating a Coin with kwargs."""
        return self.Coin(**kwargs)


class GenImporter(BaseImporter):
    """An importer that takes no arguments and just generates coins."""

    def run(self):
        """Returns the result of creating a Coin from generation."""
        return super().run()


class WifImporter(BaseImporter):
    """An importer that takes imports using a wif string."""

    def run(self, wif=None):
        """Returns the result of creating a Coin from wif."""
        if wif is None:
            wif = self.prompt.prompt_info(name="WIF key", type_f=str)
        return super().run(wif=wif)


class AddrImporter(BaseImporter):
    """An importer that takes imports using a addr string."""

    def run(self, addr=None):
        """Returns the result of creating a Coin from addr."""
        if addr is None:
            addr = self.prompt.prompt_info(name="Public address", type_f=str)
        return super().run(addr=addr)


class BrainImporter(BaseImporter):
    """An importer for brainwallets using sha256."""

    def run(self, brain=None):
        """Uses brainwallet string given to make a private key."""
        if brain is None:
            brain = self.prompt.prompt_pass(name="Brain phrase", type_f=str)

        brain_data = data.StringData(brain)
        priv = mods.Sha256(brain_data)
        return super().run(priv=priv)
