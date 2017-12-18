from pyperlib import data
import hashlib

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
    def mod(self, d):
        pass

class Slice(Mod):
    def mod(self, d, i=None, j=None, k=None):
        return d[i:j:k]

class Scrypt(Mod):
    def mod(self, d):
        pass

class Aes256(Mod):
    def mod(self, d):
        pass

class Keccak(Mod):
    def mod(self, d):
        pass
