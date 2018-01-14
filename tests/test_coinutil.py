from pyperlib import coinutil, data
from unittest import TestCase
from pyperlib.coins.basecoin import Coin as BaseCoin


class TestCoinFactory(TestCase):
    """A TestCase for the CoinFactory class."""

    def do_test(self, name, cf):
        """Check that the coinfactory has the coin and can load it."""
        self.assertTrue(cf.has(name))
        try:
            c = cf.get(name)
        except NotImplementedError:
            return
        self.assertTrue(issubclass(c, BaseCoin))

    def tests(self):
        """Check all coins in the list, as well as the current top 3."""
        cf = coinutil.CoinFactory
        for name in cf.list():
            self.do_test(name, cf)
        self.do_test('bitcoin', cf)
        self.do_test('ethereum', cf)
        self.do_test('litecoin', cf)
