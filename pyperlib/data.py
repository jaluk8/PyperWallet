from pyperlib import helper
import unicodedata


class EncodingException(Exception):
    """Occurs when invalid characters exist during conversion."""


class DataFactory(helper.NameFactory):
    """A factory to produce data objects based on their name."""
    suffix = "Data"
    pool = globals()


class BaseData:
    """The base class for all data types."""

    base58_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

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
            b58 = self.base58_chars[i] + b58
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

    def export(self, t):
        """Export from Data to type t."""
        if t is ByteData:
            return self.bytes
        elif t is HexData:
            return self.hex
        elif t is Base58Data:
            return self.base58
        elif t is IntData:
            return self.int
        elif t is StringData:
            return self.string

    def __eq__(self, other):
        """Determine the equality of two Data objects."""
        if issubclass(type(other), BaseData):
            return self.bytes == other.bytes
        else:
            return False

    def __hash__(self):
        """Return the hash of the Data."""
        return hash(self.bytes)

    def __add__(self, other):
        """Concatenate two pieces of Data."""
        d = ByteData(self.bytes + other.bytes)
        return d

    def __len__(self):
        """Return the length in bytes."""
        return len(self.bytes)

    def __getitem__(self, key):
        """Return Data from an index or slice."""
        if type(key) is slice:
            bts = self.bytes.__getitem__(key)
            return ByteData(bts)
        else:
            i = self.bytes[key]
            return IntData(i, 1)

    def __repr__(self):
        """Represents the Data as a HexData string."""
        return "HexData('" + self.hex + "')"


class ByteData(BaseData):
    """A main data class that can convert between various needed data types."""

    def __init__(self, b=b''):
        """Construct Data from bytes."""
        assert type(b) is bytes
        self.bytes = b


class HexData(BaseData):
    """A separate constructor for the data class that uses hex strings."""

    def __init__(self, s=""):
        """Construnct Data from a hex string."""
        assert type(s) is str
        self.bytes = bytes.fromhex(s)


class Base58Data(BaseData):
    """A separate constructor for the data class that uses base58 strings."""

    def __init__(self, b58=""):
        """Construct Data from a base58 string."""
        assert type(b58) is str

        value = 0
        place = 1
        for c in b58[::-1]:
            if c not in self.base58_chars:
                raise EncodingException(
                    c + " is not a valid base58 character.")
            value += place * self.base58_chars.find(c)
            place *= 58

        data = IntData(value)

        for c in b58:
            if c == '1':
                data = ByteData(b'\x00') + data
            else:
                break

        self.bytes = data.bytes


class IntData(BaseData):
    """A separate constructor for the data class that uses ints."""

    def __init__(self, i, size=0):
        """Construct Data from an int and a data size."""
        byte_value = i.to_bytes((i.bit_length() + 7) // 8, 'big', signed=False)

        while len(byte_value) < size:
            byte_value = b'\x00' + byte_value

        self.bytes = byte_value


class StringData(BaseData):
    """A separate constructor for the data class that uses encoded strings."""

    def __init__(self, s, encoding="utf-8", normalize=None):
        """Construct Data from an encoded string."""
        if normalize is not None:
            s = unicodedata.normalize(normalize, s)
        bts = s.encode(encoding)
        self.bytes = bts
