from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from pyperlib import data

SECP256K1 = ec.SECP256K1

class KeyPair:
    def __init__(self, curve, priv=None):
        self.curve = curve()
        if priv is None:
            self.gen()
        else:
            self.load(priv)

    def gen(self):
        key = ec.generate_private_key(self.curve, default_backend())
        numbers = key.private_numbers()
        self.set_privnumbers(numbers)

    def load(self, priv):
        key = ec.derive_private_key(priv.int, self.curve, default_backend())
        numbers = key.private_numbers()
        self.set_privnumbers(numbers)

    def set_privnumbers(self, privnumbers):
        self.private_numbers = privnumbers
        self.public_numbers = privnumbers.public_numbers
        
        priv_int = privnumbers.private_value
        self.priv = data.Data.fromint(priv_int, self.curve.key_size//8)

        x_int = self.public_numbers.x
        y_int = self.public_numbers.y

        coord_size = (self.curve.key_size//8 - 1) // 2
        x_data = data.Data.fromint(x_int, coord_size)
        y_data = data.Data.fromint(y_int, coord_size)

        if y_int % 2 == 0:
            prefix = b'\x02'
        else:
            prefix = b'\x03'
        
        uncompressed = data.Data(b'\x04') + x_data + y_data
        compressed = data.Data(prefix) + x_data
        self.pub_u = uncompressed
        self.pub_c = compressed
        
        assert len(self.priv.bytes) == self.curve.key_size//8

    def pub(self, compressed):
        if compressed:
            return self.pub_c
        else:
            return self.pub_u
