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
        self.assertEqual(data.frombase58(s).bytes, b)
        self.assertEqual(data.frombase58(s).base58, s)
    def test_set(self):
        self.do_test(b'\x00', '1')
        self.do_test(b'\x56', '2V')
        self.do_test(b'\x00\x00\x56\x2F', '117ZQ')
        self.do_test(b'\xcf\xde\x8e\x892\xa4\xbf\xe9\xed/\xf5\xa2\x8bb\xdfU\xe7\x8a\xc9PcavK', '1Kx7VE4M41HuS96xqArvSHY8C8xfRjHvb4')
