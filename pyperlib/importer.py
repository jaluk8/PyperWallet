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
        return self.Coin(**kwargs, prompt=self.prompt)


class GenImporter(BaseImporter):
    """An importer that takes no arguments and just generates coins."""

    description = "generate a new coin using random numbers"

    def run(self):
        """Returns the result of creating a Coin from generation."""
        return super().run()


class PromptImporter(BaseImporter):
    """An importer that imports by prompting a wif/priv/addr/etc."""

    description = "import the coin from a wif key, address, private key, etc."

    def run(self, key=None):
        """Return the result of creating a Coin from something."""
        if key is None:
            key = self.prompt.prompt_info(name="Key", type_f=str)
        return super().run(key=key)


class BrainImporter(BaseImporter):
    """An importer for brainwallets using sha256."""

    description = "import the coin using a memorized 'brain wallet' phrase"

    def run(self, brain=None):
        """Uses brainwallet string given to make a private key."""
        if brain is None:
            brain = self.prompt.prompt_pass(name="Brain phrase", type_f=str)

        brain_data = data.StringData(brain)
        priv = mods.Sha256(brain_data)
        return super().run(key=priv)
