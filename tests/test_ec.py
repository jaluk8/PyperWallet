from unittest import TestCase
from pyperlib import ec
from pyperlib import data

class Test(TestCase):
    def load(self, curve, priv, pub):
        e = ec.KeyPair(curve, priv)
        self.assertEqual(type(e.priv), data.Data)
        self.assertEqual(type(e.pub), data.Data)

        self.assertEqual(e.priv == priv)
        self.assertEqual(e.pub == pub)
        
    def gen(self, curve):
        e = ec.KeyPair(curve)
        self.load(curve, e.priv, e.pub)

    def test_set(self):
        self.gen("secp256k1")
