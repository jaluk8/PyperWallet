from unittest import TestCase
from pyperlib import ec
from pyperlib import data

ex_priv = data.HexData('AEFA9CD9F498E6E0929277CD19FE8699D343582A6A6C5C8A79C6D76444DCE942')
ex_pubu = data.HexData('040BF82C0EC3CB07FE72F5DCB264624A9CF775CC996B64778C6FA7E1462C119B'+
                            'D3FA2E796B504AA3FCF4D4022D107858D988D4793EBE538670877C8F72E438FDC7')
ex_pubc = data.HexData('030BF82C0EC3CB07FE72F5DCB264624A9CF775CC996B64778C6FA7E1462C119BD3')

class TestPriv(TestCase):
    """A TestCase for construction from private Data."""

    def load(self, curve, priv, pub_u, pub_c):
        """Check if data is correct after loading a priv."""
        e = ec.KeyPair(curve, priv=priv)

        self.assertEqual(e.priv, priv)
        self.assertEqual(e.pub_u, pub_u)
        self.assertEqual(e.pub_c, pub_c)
        
    def gen(self, curve):
        """Generate a private key and check it."""
        e = ec.KeyPair(curve)
        self.load(curve, e.priv, e.pub_u, e.pub_c)

    def test_set(self):
        """Generate keys and check a sample key."""
        for x in range(100):
            self.gen(ec.SECP256K1)
        self.load(ec.SECP256K1, ex_priv, ex_pubu, ex_pubc)

class TestPubU(TestCase):
    """A TestCase for construction from uncompressed public Data."""

    def load_u(self, curve, pub_u, pub_c):
        """Check if data is correct after loading a pub_u."""
        e = ec.KeyPair(curve, pub=pub_u)

        self.assertEqual(e.priv, None)
        self.assertEqual(e.pub_u, pub_u)
        self.assertEqual(e.pub_c, pub_c)

    def test_set(self):
        """Check the example data with load_u."""
        self.load_u(ec.SECP256K1, ex_pubu, ex_pubc)

class TestPubC(TestCase):
    """A TestCase for construction from compressed public Data."""

    def load_c(self, curve, pub_c):
        """Check if data is correct after loading a pub_c."""
        e = ec.KeyPair(curve, pub=pub_c)

        self.assertEqual(e.priv, None)
        self.assertEqual(e.pub_u, None)
        self.assertEqual(e.pub_c, pub_c)

    def test_set(self):
        """Check the example data with load_c."""
        self.load_c(ec.SECP256K1, ex_pubc)
