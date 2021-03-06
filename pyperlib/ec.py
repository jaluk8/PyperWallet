from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from pyperlib import data

SECP256K1 = ec.SECP256K1


class KeyPair:
    """A set of private and public keys described as Data objects."""

    def __init__(self, curve, *, priv=None, pub=None):
        """Construct a KeyPair from a curve and possibly a key."""
        self.curve = curve()
        self.priv = None
        self.pub_u = None
        self.pub_c = None

        if priv is not None:
            self.load_priv(priv)
        elif pub is not None:
            self.load_pub(pub)
        else:
            self.gen()

    def gen(self):
        """Generate private/public keys randomly."""
        self.priv = data.ByteData(b'\x00')
        # Some coins (ETH) do not allow leading zeroes in private keys.
        while self.priv.bytes[0] == 0:
            key = ec.generate_private_key(self.curve, default_backend())
            self.set_priv(key)

    def load_priv(self, priv):
        """Set the private/public keys from a private Data object."""
        key = ec.derive_private_key(priv.int, self.curve, default_backend())
        self.set_priv(key)

    def load_pub(self, pub):
        """Set the public keys from a public Data object."""
        t = pub[0].hex
        if t == '04':
            coord_len = len(pub) // 2 + 1
            x = pub[1:coord_len].int
            y = pub[coord_len:].int
            self.set_pub(x, y)
        else:
            self.pub_c = pub

    def set_priv(self, priv):
        """Set the private/public keys from a PrivateKey object."""
        privnumbers = priv.private_numbers()
        self.private_numbers = privnumbers
        self.public_numbers = privnumbers.public_numbers

        priv_int = privnumbers.private_value
        self.priv = data.IntData(priv_int, self.curve.key_size // 8)

        x_int = self.public_numbers.x
        y_int = self.public_numbers.y

        self.set_pub(x_int, y_int)

        assert len(self.priv) == self.curve.key_size // 8

    def set_pub(self, x, y):
        """Set the public keys from x and y coordinates."""
        coord_size = (self.curve.key_size // 8)
        x_data = data.IntData(x, coord_size)
        y_data = data.IntData(y, coord_size)

        if y % 2 == 0:
            prefix = b'\x02'
        else:
            prefix = b'\x03'

        uncompressed = data.ByteData(b'\x04') + x_data + y_data
        compressed = data.ByteData(prefix) + x_data
        self.pub_u = uncompressed
        self.pub_c = compressed

        assert len(self.pub_u) == self.curve.key_size // 4 + 1
        assert len(self.pub_c) == self.curve.key_size // 8 + 1

    def pub(self, compressed):
        """Return a compressed or uncompressed public Data object."""
        if compressed:
            return self.pub_c
        else:
            return self.pub_u

    def is_compressed(self, pub):
        """Check whether the given public key is compressed."""
        if type(self.curve) is SECP256K1:
            return pub[0].hex != "04"
