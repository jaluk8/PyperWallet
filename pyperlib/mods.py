from pyperlib import data
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class LengthError(Exception):
    pass

class Mod(data.Data):
    def __init__(self, *args):
        self.bytes = self.mod(*args).bytes
    def mod(self, d):
        raise NotImplementedError

class HashMod(Mod):
    def mod(self, d):
        h = hashlib.new(self.algorithm)
        h.update(d.bytes)
        bts = h.digest()
        return data.Data(bts)

class Sha256(HashMod):
    algorithm = 'sha256'

class Ripemd160(HashMod):
    algorithm = 'ripemd160'

class Concat(Mod):
    def mod(self, *args):
        return sum(args, data.Data())

class Xor(Mod):
    def mod(self, d1, d2):
        l = len(d1)
        if l != len(d2):
            raise LengthError("Both operands of xor must have the same length.")
        i = d1.int ^ d2.int
        return data.Data.fromint(i, l)

class Slice(Mod):
    def mod(self, d, i=None, j=None, k=None):
        return d[i:j:k]

class Scrypt(Mod):
    def mod(self, password, salt):
        bts = hashlib.scrypt(password.bytes, salt=salt.bytes, n=16384, r=8, p=8, dklen=64)
        return data.Data(bts)

class Aes256(Mod):
    def cipher(self, key):
        alg = algorithms.AES(key.bytes)
        mode = modes.ECB()
        return Cipher(alg, mode, backend=default_backend())
    def run_cipher(self, context, block):
        result = context.update(block.bytes)
        result += context.finalize()
        return data.Data(result)

class Aes256Enc(Aes256):
    def mod(self, block, key):
        context = self.cipher(key).encryptor()
        return self.run_cipher(context, block)

class Aes256Dec(Aes256):
    def mod(self, block, key):
        context = self.cipher(key).decryptor()
        return self.run_cipher(context, block)

class Keccak(Mod):
    def mod(self, d):
        pass
