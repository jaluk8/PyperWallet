from pyperlib import importer, coins, cryptor, exporter, prompter


class ArgumentError(Exception):
    """Raise when an argument, such as the importer, is invalid."""


class Wallet:
    """A high-level interface for manipulating coins."""

    coin_f = coins.CoinFactory()
    importer_f = importer.ImporterFactory
    cryptor_f = cryptor.CryptorFactory
    exporter_f = exporter.ExporterFactory

    def __init__(self, Coin, Importer, Exporter, Prompt=None, Cryptor=None,
                 settings=None, **kwargs):
        """Create a Wallet from any coin-manipulating objects."""

        self.Coin = Coin
        self.Importer = Importer
        self.Exporter = Exporter
        self.Prompt = Prompt
        self.Cryptor = Cryptor
        self.settings = settings

        if settings is None:
            self.settings = coins.CoinSettings(**kwargs)

        if type(Coin) is str:
            self.Coin = self.coin_f.get_coin(Coin)
        if type(Importer) is str:
            self.Importer = self.importer_f.get(Importer)
        if type(Exporter) is str:
            self.Exporter = self.exporter_f.get(Exporter)
        if Cryptor is not None and type(Cryptor) is str:
            self.Cryptor = self.cryptor_f.get(Cryptor)
            if self.Cryptor is None:
                raise ArgumentError("Invalid Cryptor")

        if self.Coin is None:
            raise ArgumentError("Invalid Coin")
        if self.Importer is None:
            raise ArgumentError("Invalid Importer")
        if self.Exporter is None:
            raise ArgumentError("Invalid Exporter")

    def run(self):
        """Import the coin, perform any modifications, and export it."""
        i = self.Importer(self.Coin, self.Prompt)
        coin = i.run()

        if self.settings is not None:
            coin.settings = self.settings
        coin.calc_all()

        if self.Cryptor is not None:
            c = self.Cryptor(self.Prompt)
            c.encrypt(coin)

        e = self.Exporter()
        e.run(coin)
