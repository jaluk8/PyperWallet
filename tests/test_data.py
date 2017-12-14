from unittest import TestCase
from pyperlib import data

class TestDataBytes(TestCase):
    def do_test(self, b):
        self.assertEqual(data.Data(b).bytes, b)
    def test_set(self):
        self.do_test(b'\x00')
        self.do_test(b'\xFF\x10\x25')
        self.do_test(b'\x00\x00\x10')

class TestDataHex(TestCase):
    def do_test(self, b, s):
        self.assertEqual(data.Data(b).hex, s)
        self.assertEqual(data.Data.fromhex(s).bytes, b)
        self.assertEqual(data.Data.fromhex(s).hex, s)
    def test_set(self):
        self.do_test(b'\x00', '00')
        self.do_test(b'\xFF\x10', 'FF10')
        self.do_test(b'\x00\x00\x10', '000010')

class TestDataBase58(TestCase):
    def do_test(self, b, s):
        self.assertEqual(data.Data(b).base58, s)
        self.assertEqual(data.Data.frombase58(s).bytes, b)
        self.assertEqual(data.Data.frombase58(s).base58, s)
    def test_set(self):
        self.do_test(b'\x00', '1')
        self.do_test(b'\x56', '2V')
        self.do_test(b'\x00\x00\x56\x2F', '117ZQ')
        self.do_test(b'\x00\xcf\xde\x8e\x892\xa4\xbf\xe9\xed/\xf5\xa2\x8bb\xdfU\xe7\x8a\xc9PcavK', '1Kx7VE4M41HuS96xqArvSHY8C8xfRjHvb4')

class TestAppend(TestCase):
    def test_append(self):
        d = data.Data.fromhex('0011FF')
        d.append(data.Data.fromhex('55'))
        self.assertEqual(d.hex, '0011FF55')
    def test_prepend(self):
        d = data.Data.fromhex('4568FA')
        d.prepend(data.Data.fromhex('00'))
        self.assertEqual(d.hex, '004568FA')

class TestEqual(TestCase):
    def eq(self, d, b):
        self.assertTrue(d == data.Data(b))
    def neq(self, d, b):
        self.assertFalse(d == data.Data(b))
    def test_set(self):
        tests = [data.Data(b'\x00\xFA\x04'),
                 data.Data.fromhex("00FE45A3"),
                 data.Data.frombase58("1HjKoPaS2")]
        for i in range(len(tests)):
            j = (i + 1) % len(tests)
            self.eq(tests[i], tests[i].bytes)
            self.neq(tests[i], tests[j].bytes)
