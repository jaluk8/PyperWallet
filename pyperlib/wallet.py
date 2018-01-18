from pyperlib import importer, coins, coinutil, cryptor, exporter, prompter
import sys


class ArgumentError(Exception):
    """Raise when an argument, such as the importer, is invalid."""


class Wallet:
    """A high-level interface for manipulating coins."""

    coin_f = coinutil.CoinFactory
    importer_f = importer.ImporterFactory
    cryptor_f = cryptor.CryptorFactory
    exporter_f = exporter.ExporterFactory
    Settings = coins.CoinSettings()

    def __init__(self, Coin, Importer, Exporter, Prompt, Cryptor=None,
                 out_file=None, debug=False, **kwargs):
        """Create a Wallet from any coin-manipulating objects."""

        self.Coin = Coin
        self.Importer = Importer
        self.Exporter = Exporter
        self.Prompt = Prompt
        self.Cryptor = Cryptor
        self.out_file = out_file
        self.debug = debug
        self.kwargs = kwargs

        if type(Coin) is str:
            self.Coin = self.coin_f.get(Coin)
        if type(Importer) is str:
            self.Importer = self.importer_f.get(Importer)
        if type(Exporter) is str:
            self.Exporter = self.exporter_f.get(Exporter)
        if Cryptor is not None and type(Cryptor) is str:
            self.Cryptor = self.cryptor_f.get(Cryptor)

        if self.Coin is None:
            raise ArgumentError("Invalid Coin")
        if self.Importer is None:
            raise ArgumentError("Invalid Importer")
        if self.Exporter is None:
            raise ArgumentError("Invalid Exporter")

    def run(self):
        """Import the coin, perform any modifications, and export it."""
        prompt = self.Prompt()
        if self.debug:
            prompt.pass_input = input

        i = self.Importer(self.Coin, prompt)
        coin = i.run()

        coin.apply_settings(**self.kwargs)
        coin.calc_all()

        if self.Cryptor is not None:
            c = self.Cryptor(prompt)
            c.encrypt(coin)

        e = self.Exporter(self.out_file)
        return e.run(coin)
