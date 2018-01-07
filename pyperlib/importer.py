from pyperlib import data, mods


class BaseImporter:
    """An importer that imports using args, rather than external sources."""

    def __init__(self, Coin):
        """Initializes the importer with a Coin class."""
        self.Coin = Coin

    def run(self, **kwargs):
        """Returns the result of creating a Coin with kwargs."""
        return self.Coin(**kwargs)


class GenImporter(BaseImporter):
    """An importer that takes no arguments and just generates coins."""

    def run(self):
        """Returns the result of creating a Coin from generation."""
        return super().run()


class CliImporter(BaseImporter):
    """An importer that takes the arguments from stdin."""

    def run(self):
        """Returns the result of creating a Coin from stdin."""
        t = input("Choose a data type to input (wif/view/addr): ")
        while t not in ["wif", "view", "addr"]:
            t = input("You must enter wif, view, or addr: ")

        if t == "wif":
            wif = input("Enter WIF key: ")
            return super().run(wif=wif)
        elif t == "view":
            view = input("Enter view key: ")
            return super().run(view=view)
        elif t == "addr":
            addr = input("Enter address: ")
            return super().run(addr=addr)


class BaseBrainImporter(BaseImporter):
    """An importer for brainwallets using sha256."""

    def run(self, brain):
        """Uses brainwallet string given to make a private key."""
        brain_data = data.StringData(brain)
        priv = mods.Sha256(brain_data)
        return super().run(priv=priv)
