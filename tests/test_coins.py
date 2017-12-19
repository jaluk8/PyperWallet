from pyperlib import coins
from unittest import TestCase

class TestCoinList(TestCase):
    def do_test(self, name, cl):
        self.assertTrue(cl.has_coin(name))
        c = cl.get_coin(name)
        self.assertTrue(issubclass(c, coins.BaseCoin))
    def tests(self):
        cl = coins.CoinList()
        for name in cl.list_coins():
            self.do_test(name, cl)
        self.do_test('btc', cl)
        self.do_test('eth', cl)
        self.do_test('ltc', cl)

class TestBaseCoin(TestCase):
    pass

class TestAllCoins(TestCase):
    pass
