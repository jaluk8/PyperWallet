from unittest import TestCase
from pyperlib import ec
from pyperlib import data

ex_priv = data.Data.fromhex('AEFA9CD9F498E6E0929277CD19FE8699D343582A6A6C5C8A79C6D76444DCE942')
ex_pubu = data.Data.fromhex('040BF82C0EC3CB07FE72F5DCB264624A9CF775CC996B64778C6FA7E1462C119B'+
                            'D3FA2E796B504AA3FCF4D4022D107858D988D4793EBE538670877C8F72E438FDC7')
ex_pubc = data.Data.fromhex('030BF82C0EC3CB07FE72F5DCB264624A9CF775CC996B64778C6FA7E1462C119BD3')

class TestPriv(TestCase):
    def load(self, curve, priv, pub_u, pub_c):
        e = ec.KeyPair(curve, priv=priv)
        self.assertEqual(type(e.priv), data.Data)
        self.assertEqual(type(e.pub_u), data.Data)
        self.assertEqual(type(e.pub_c), data.Data)

        self.assertEqual(e.priv, priv)
        self.assertEqual(e.pub_u, pub_u)
        self.assertEqual(e.pub_c, pub_c)
        
    def gen(self, curve):
        e = ec.KeyPair(curve)
        self.load(curve, e.priv, e.pub_u, e.pub_c)

    def test_set(self):
        for x in range(100):
            self.gen(ec.SECP256K1)
        self.load(ec.SECP256K1, ex_priv, ex_pubu, ex_pubc)

class TestPubU(TestCase):
    def load_u(self, curve, pub_u, pub_c):
        e = ec.KeyPair(curve, pub=pub_u)
        self.assertEqual(e.priv, None)
        self.assertEqual(type(e.pub_u), data.Data)
        self.assertEqual(type(e.pub_c), data.Data)

        self.assertEqual(e.pub_u, pub_u)
        self.assertEqual(e.pub_c, pub_c)

    def test_set(self):
        self.load_u(ec.SECP256K1, ex_pubu, ex_pubc)

class TestPubC(TestCase):
    def load_c(self, curve, pub_c):
        e = ec.KeyPair(curve, pub=pub_c)
        self.assertEqual(e.priv, None)
        self.assertEqual(e.pub_u, None)
        self.assertEqual(type(e.pub_c), data.Data)
        self.assertEqual(e.pub_c, pub_c)

    def test_set(self):
        self.load_c(ec.SECP256K1, ex_pubc)
