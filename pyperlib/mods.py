from pyperlib import data
import hashlib
import sha3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class LengthError(Exception):
    """An Exception that occurs when Data is of improper length."""

class Mod(data.Data):
    """The base class for Mods that alter Data through the Algorithm design pattern."""
    def __init__(self, *args):
        """Construnct the mod and run mod(*args)."""
        self.bytes = self.mod(*args).bytes
    def mod(self, d):
        """Execute the mod."""
        raise NotImplementedError

class HashMod(Mod):
    """An abstract Mod that gets a hash of Data."""

    def mod(self, d):
        """Execute the hash."""
        h = self.algorithm()
        h.update(d.bytes)
        bts = h.digest()
        return data.Data(bts)

class Sha256(HashMod):
    """A HashMod using sha256."""

    def algorithm(self):
        """Execute the hash."""
        return hashlib.new('sha256')

class Ripemd160(HashMod):
    """A HashMod using ripemd160."""

    def algorithm(self):
        """Execute the hash."""
        return hashlib.new('ripemd160')

class Keccak(HashMod):
    """A HashMod using keccak (NOT SHA3)."""

    def algorithm(self):
        """Execute the hash."""
        return sha3.keccak_256()

class Concat(Mod):
    """A Mod that concats two pieces of Data."""

    def mod(self, *args):
        """Execute the mod."""
        return sum(args, data.Data())

class Xor(Mod):
    """A Mod that performs xor on two pieces of Data."""

    def mod(self, d1, d2):
        """Execute the mod."""
        l = len(d1)
        if l != len(d2):
            raise LengthError("Both operands of xor must have the same length.")
        i = d1.int ^ d2.int
        return data.Data.fromint(i, l)

class Slice(Mod):
    """A Mod that performs slicing on Data."""

    def mod(self, d, i=None, j=None, k=None):
        """Execute the mod."""
        return d[i:j:k]

class Scrypt(Mod):
    """A Mod that performs SCrypt key derivation for bip38."""

    def mod(self, password, salt):
        """Execute the mod."""
        bts = hashlib.scrypt(password.bytes, salt=salt.bytes, n=16384, r=8, p=8, dklen=64)
        return data.Data(bts)

class Aes256(Mod):
    """A base Mod for aes256 operations."""

    def cipher(self, key):
        """Return a Cipher object for given key Data."""
        alg = algorithms.AES(key.bytes)
        mode = modes.ECB()
        return Cipher(alg, mode, backend=default_backend())

    def run_cipher(self, context, block):
        """Return Data from running an action on a Cipher object."""
        result = context.update(block.bytes)
        result += context.finalize()
        return data.Data(result)

class Aes256Enc(Aes256):
    """A Mod that encrypts aes256."""

    def mod(self, block, key):
        """Execute the mod."""
        context = self.cipher(key).encryptor()
        return self.run_cipher(context, block)

class Aes256Dec(Aes256):
    """A Mod that decrypts aes256."""

    def mod(self, block, key):
        """Execute the mod."""
        context = self.cipher(key).decryptor()
        return self.run_cipher(context, block)
