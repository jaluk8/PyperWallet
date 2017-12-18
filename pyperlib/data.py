base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

class EncodingException(Exception):
    pass

class Data:
    """The generic data class for PyperWallet.
    It can convert between various needed data types."""
    def __init__(self, b):
        assert type(b) is bytes
        self.bytes = b

    @staticmethod
    def fromhex(s):
        assert type(s) is str
        return Data(bytes.fromhex(s))

    @staticmethod
    def frombase58(b58):
        assert type(b58) is str
        
        value = 0
        place = 1
        for c in b58[::-1]:
            if not c in base58:
                raise EncodingException(c + " is not a valid base58 character.")
            value += place * base58.find(c)
            place *= 58

        data = Data.fromint(value)

        for c in b58:
            if c == '1':
                data.prepend(Data(b'\x00'))
            else:
                break
        
        return data

    @staticmethod
    def fromint(i, size=0):
        byte_value = i.to_bytes((i.bit_length() + 7) // 8, 'big', signed=False)
        data = Data(byte_value)
        
        while len(data.bytes) < size:
            data.prepend(Data(b'\x00'))

        return data
    
    @property
    def hex(self):
        return self.bytes.hex().upper()

    @property
    def int(self):
        return int.from_bytes(self.bytes, byteorder='big', signed=False)

    @property
    def base58(self):
        value = self.int
        b58 = ""

        while value > 0:
            i = value % 58
            b58 = base58[i] + b58
            value //= 58

        for b in self.bytes:
            if b == 0:
                b58 = '1' + b58
            else:
                break

        return b58

    @property
    def string(self):
        return self.hex # To be overriden
    
    def append(self, d):
        self.bytes = self.bytes + d.bytes

    def prepend(self, d):
        self.bytes = d.bytes + self.bytes

    def __eq__(self, other):
        return self.bytes == other.bytes

    def __hash__(self):
        return hash(self.bytes)

    def __add__(self, other):
        d = Data(self.bytes)
        d.append(other)
        return d

    def __getitem__(self, key):
        if type(key) is slice:
            bts = self.bytes.__getitem__(key)
            return Data(bts)
        else:
            i = self.bytes[key]
            return Data.fromint(i, 1)
