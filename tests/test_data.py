from unittest import TestCase
from pyperlib import data

class TestDataBytes(TestCase):
    """A TestCase for bytes conversion."""

    def do_test(self, b):
        """Check construction from bytes."""
        self.assertEqual(data.Data(b).bytes, b)
    def test_set(self):
        """Check various data."""
        self.do_test(b'\x00')
        self.do_test(b'\xFF\x10\x25')
        self.do_test(b'\x00\x00\x10')

class TestDataHex(TestCase):
    """A TestCase for hex string conversion."""

    def do_test(self, b, s):
        """Check construction from hex."""
        self.assertEqual(data.Data(b).hex, s)
        self.assertEqual(data.Data.fromhex(s).bytes, b)
        self.assertEqual(data.Data.fromhex(s).hex, s)
    def test_set(self):
        """Check various data."""
        self.do_test(b'\x00', '00')
        self.do_test(b'\xFF\x10', 'FF10')
        self.do_test(b'\x00\x00\x10', '000010')

class TestDataInt(TestCase):
    """A TestCase for int value conversion."""

    def do_test(self, b, i):
        """Check construction from int."""
        self.assertEqual(data.Data(b).int, i)
        self.assertEqual(data.Data.fromint(i, len(b)).bytes, b)
        self.assertEqual(data.Data.fromint(i, len(b)).int, i)
    def test_set(self):
        """Check various data."""
        self.do_test(b'\x00', 0)
        self.do_test(b'\x50\xF3', 20723)
        self.do_test(b'\x00\x50\xF3', 20723)

class TestDataBase58(TestCase):
    """A TestCase for base58 string conversion."""

    def do_test(self, b, s):
        """Check construction from base58."""
        self.assertEqual(data.Data(b).base58, s)
        self.assertEqual(data.Data.frombase58(s).bytes, b)
        self.assertEqual(data.Data.frombase58(s).base58, s)
    def test_set(self):
        """Check various data."""
        self.do_test(b'\x00', '1')
        self.do_test(b'\x56', '2V')
        self.do_test(b'\x00\x00\x56\x2F', '117ZQ')
        self.do_test(b'\x00\xcf\xde\x8e\x892\xa4\xbf\xe9\xed/\xf5\xa2\x8bb\xdfU\xe7\x8a\xc9PcavK', '1Kx7VE4M41HuS96xqArvSHY8C8xfRjHvb4')

class TestDataString(TestCase):
    """A TestCase for encoded string conversion."""

    def do_test(self, b, s):
        """Check construction from string."""
        self.assertEqual(data.Data(b).string, s)
        self.assertEqual(data.Data.fromstring(s).bytes, b)
        self.assertEqual(data.Data.fromstring(s).string, s)
    def test_set(self):
        """Check various data."""
        self.do_test(b'\x41', "A")
        self.do_test(b'\xCF\x80', u'\u03C0')
        self.do_test(b'Hello', u'Hello')

class TestAppend(TestCase):
    """A TestCase for Data append and prepend."""

    def test_append(self):
        """Check Data.append."""
        d = data.Data.fromhex('0011FF')
        d.append(data.Data.fromhex('55'))
        self.assertEqual(d.hex, '0011FF55')
    def test_prepend(self):
        """Check Data.prepend."""
        d = data.Data.fromhex('4568FA')
        d.prepend(data.Data.fromhex('00'))
        self.assertEqual(d.hex, '004568FA')

class TestEqual(TestCase):
    """A TestCase for Data equality."""

    def eq(self, d, b):
        """Check that two Data objects are equal."""
        self.assertTrue(d == data.Data(b))
    def neq(self, d, b):
        """Check that two Data objects are not equal."""
        self.assertFalse(d == data.Data(b))
    def test_set(self):
        """Check equality relations for 3 Data."""
        tests = [data.Data(b'\x00\xFA\x04'),
                 data.Data.fromhex("00FE45A3"),
                 data.Data.frombase58("1HjKoPaS2")]
        for i in range(len(tests)):
            j = (i + 1) % len(tests)
            self.eq(tests[i], tests[i].bytes)
            self.neq(tests[i], tests[j].bytes)

class TestAdd(TestCase):
    """A TestCase for Data concatenation."""

    def addition(self, a, b, c):
        """Check that a+b=c."""
        self.assertEqual(data.Data(a), data.Data(b) + data.Data(c))
    def test_set(self):
        """Check various data."""
        self.addition(b'\x01\x02', b'\x01', b'\x02')
        self.addition(b'\xE8\x0A', b'\xE8', b'\x0A')
        self.addition(b'\x01\x00\x01', b'\x01', b'\x00\x01')

class TestSlice(TestCase):
    """A TestCase for Data slicing."""

    def slice(self, in_hex, out_hex, *args):
        """Check that in_hex[args] = out_hex."""
        din = data.Data.fromhex(in_hex)
        dout = data.Data.fromhex(out_hex)
        dresult = din.__getitem__(*args)
        self.assertEqual(dout, dresult)
    def test_set(self):
        """Check various data."""
        self.slice("AABBCC", "AA", 0)
        self.slice("AABBCC", "CC", -1)
        self.slice("AABBCC", "AABBCC", slice(None, None, None))
        self.slice("AABBCC", "BBCC", slice(1, 3, None))
        self.slice("AABBCC", "CCBBAA", slice(None, None, -1))
