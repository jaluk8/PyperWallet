from pyperlib import data


class BaseImporter:
    """An importer that imports using args, rather than external sources."""

    def __init__(self, Coin):
        """Initializes the importer with a Coin class."""
        self.Coin = Coin

    def run(self, **kwargs):
        """Returns the result of creating a Coin with kwargs."""
        return self.Coin(**kwargs)
