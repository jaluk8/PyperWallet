from pyperlib import importer, coins, coinutil, cryptor, exporter, prompter
import sys


__all__ = ["ArgumentError", "Wallet", "cliwallet"]


class ArgumentError(Exception):
    """Raise when an argument, such as the importer, is invalid."""


class Wallet:
    """A high-level interface for manipulating coins."""

    coin_f = coinutil.CoinFactory
    importer_f = importer.ImporterFactory
    cryptor_f = cryptor.CryptorFactory
    exporter_f = exporter.ExporterFactory
    Settings = coins.CoinSettings()

    def __init__(self, Coin, Importer, Exporter, prompt, Cryptor=None,
                 out_file=None, debug=False, **kwargs):
        """Create a Wallet from any coin-manipulating objects."""

        self.Coin = Coin
        self.Importer = Importer
        self.Exporter = Exporter
        self.prompt = prompt
        self.Cryptor = Cryptor
        self.out_file = out_file
        self.debug = debug
        self.kwargs = kwargs

    @property
    def Coin(self):
        """Getter for the coin variable."""
        return self._Coin

    @Coin.setter
    def Coin(self, Coin):
        """Setter for the coin variable."""
        if type(Coin) is str:
            self._Coin = self.coin_f.get(Coin)
        else:
            self._Coin = Coin
        if self.Coin is None:
            raise ArgumentError("Invalid Coin")

    @property
    def Importer(self):
        """Getter for the importer variable."""
        return self._Importer

    @Importer.setter
    def Importer(self, Importer):
        """Setter for the importer variable."""
        if type(Importer) is str:
            self._Importer = self.importer_f.get(Importer)
        else:
            self._Importer = Importer
        if self.Importer is None:
            raise ArgumentError("Invalid Importer")

    @property
    def Exporter(self):
        """Getter for the exporter variable."""
        return self._Exporter

    @Exporter.setter
    def Exporter(self, Exporter):
        """Setter for the exporter variable."""
        if type(Exporter) is str:
            self._Exporter = self.exporter_f.get(Exporter)
        else:
            self._Exporter = Exporter
        if self.Exporter is None:
            raise ArgumentError("Invalid Exporter")

    @property
    def Cryptor(self):
        """Getter for the cryptor variable."""
        return self._Cryptor

    @Cryptor.setter
    def Cryptor(self, Cryptor):
        """Setter for the cryptor variable."""
        if type(Cryptor) is str:
            self._Cryptor = self.cryptor_f.get(Cryptor)
        else:
            self._Cryptor = Cryptor

    def run(self):
        """Import the coin, perform any modifications, and export it."""
        prompt = self.prompt
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
