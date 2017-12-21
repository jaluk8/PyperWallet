import unicodedata

base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

class EncodingException(Exception):
    """An Exception that occurs when invalid characters exist during conversion."""

class Data:
    """A class that can convert between various needed data types."""
    
    def __init__(self, b=b''):
        """Construct Data from bytes."""
        assert type(b) is bytes
        self.bytes = b

    @staticmethod
    def fromhex(s):
        """Construnct Data from a hex string."""
        assert type(s) is str
        return Data(bytes.fromhex(s))

    @staticmethod
    def frombase58(b58):
        """Construct Data from a base58 string."""
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
        """Construct Data from an int and a data size."""
        byte_value = i.to_bytes((i.bit_length() + 7) // 8, 'big', signed=False)
        data = Data(byte_value)
        
        while len(data.bytes) < size:
            data.prepend(Data(b'\x00'))

        return data

    @staticmethod
    def fromstring(s, encoding="utf-8", normalize=None):
        """Construct Data from an encoded string."""
        if normalize is not None:
            s = unicodedata.normalize(normalize, s)
        bts = s.encode(encoding)
        return Data(bts)
    
    @property
    def hex(self):
        """Return the hex string of the Data."""
        return self.bytes.hex().upper()

    @property
    def int(self):
        """Return the int value of the Data."""
        return int.from_bytes(self.bytes, byteorder='big', signed=False)

    @property
    def base58(self):
        """Return the base58 string of the Data."""
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
        """Return the encoded string of the Data."""
        return self.bytes.decode("utf-8")
    
    def append(self, d):
        """Append another Data object at the end."""
        self.bytes = self.bytes + d.bytes

    def prepend(self, d):
        """Prepend another Data object at the front."""
        self.bytes = d.bytes + self.bytes

    def __eq__(self, other):
        """Determine the equality of two Data objects."""
        if issubclass(type(other), Data):
            return self.bytes == other.bytes
        else:
            return False

    def __hash__(self):
        """Return the hash of the Data."""
        return hash(self.bytes)

    def __add__(self, other):
        """Concatenate two pieces of Data."""
        d = Data(self.bytes)
        d.append(other)
        return d

    def __len__(self):
        """Return the length in bytes."""
        return len(self.bytes)

    def __getitem__(self, key):
        """Return Data from an index or slice."""
        if type(key) is slice:
            bts = self.bytes.__getitem__(key)
            return Data(bts)
        else:
            i = self.bytes[key]
            return Data.fromint(i, 1)
