from unittest import TestCase
from pyperlib import mods, data

class ModTest(TestCase):
    def do_test(self, mod, o, *a):
        args = [data.Data.fromhex(i) for i in a]
        self.assertEqual(mod(*args), data.Data.fromhex(o))

class TestSha256(ModTest):
    def test(self):
        self.do_test(mods.sha256, "995DA3CF545787D65F9CED52674E92EE8171C87C7A4008AA4349EC47D21609A7", "ABCDEF")
        self.do_test(mods.sha256, "D2BDEC3101EB836B1A87AFBC37E20AAFBBD9C77D2E146DDA4C732D44C0BF4515", "00AB")
        self.do_test(mods.sha256, "8F414150ACB8F255A847C933BEB781B6B3552D502032A5F5A1374F1D2D00B877", "ACD300")

class TestRipMD160(ModTest):
    def test(self):
        self.do_test(mods.ripmd160, "A3335A6EE4A6DA99932AEEE33423DD9AFE8623D7", "ABCDEF")
        self.do_test(mods.ripmd160, "F6D37D7E7D1743BD8623D32645932CB840F858DA", "00AB")
        self.do_test(mods.ripmd160, "D1A3258B5F6EB32A452BC6F3253ABC65C0275CF6", "ACD300")

class TestConcat(ModTest):
    def test(self):
        self.do_test(mods.concat, "A53E", "A5", "3E")
        self.do_test(mods.concat, "0000AE45", "0000", "AE45")
        self.do_test(mods.concat, "A3", "", "A3")
        self.do_test(mods.concat, "00001F4E", "00", "001F4E")
        self.do_test(mods.concat, "1F00", "1F", "00")

class TestXor(ModTest):
    def test(self):
        self.do_test(mods.xor, "01", "00", "01")
        self.do_test(mods.xor, "00", "01", "01")
        self.do_test(mods.xor, "E8EC", "4321", "ABCD")
        self.do_test(mods.xor, "0012", "0a10", "0a02")
        self.do_test(mods.xor, "00A3", "0000", "00A3")

class TestSplice(ModTest):
    def splice_undo(self, i):
        d = data.Data.fromhex(i)
        d1 = mods.splice(d, 0, 2)
        d2 = mods.splice(d, 2, 4)
        dc = mods.concat(d1, d2)
        self.assertEqual(d, dc)
    def test(self):
        self.splice_undo("00112233")
        self.splice_undo("00000000")
        self.splice_undo("A64FEC23")
        self.splice_undo("00AE3400")

class TestScrypt(ModTest):
    def test(self):
        self.do_test(mods.scrypt, "", "")
        self.do_test(mods.scrypt, "", "")
        self.do_test(mods.scrypt, "", "")
        self.do_test(mods.scrypt, "", "")
        self.do_test(mods.scrypt, "", "")

class TestAes256(ModTest):
    def test(self):
        self.do_test(mods.aes256, "", "")
        self.do_test(mods.aes256, "", "")
        self.do_test(mods.aes256, "", "")
        self.do_test(mods.aes256, "", "")
        self.do_test(mods.aes256, "", "")

class TestKeccak(ModTest):
    def test(self):
        self.do_test(mods.keccak, "", "")
        self.do_test(mods.keccak, "", "")
        self.do_test(mods.keccak, "", "")
        self.do_test(mods.keccak, "", "")
        self.do_test(mods.keccak, "", "")

class TestBTCChecksum(ModTest):
    def test(self):
        self.do_test(mods.btc_checksum, "", "")
        self.do_test(mods.btc_checksum, "", "")
        self.do_test(mods.btc_checksum, "", "")
        self.do_test(mods.btc_checksum, "", "")
        self.do_test(mods.btc_checksum, "", "")

class TestBTCAddress(ModTest):
    def test(self):
        self.do_test(mods.btc_address, "", "")
        self.do_test(mods.btc_address, "", "")
        self.do_test(mods.btc_address, "", "")
        self.do_test(mods.btc_address, "", "")
        self.do_test(mods.btc_address, "", "")

class TestBTCWIF(ModTest):
    def test(self):
        self.do_test(mods.btc_wif, "", "")
        self.do_test(mods.btc_wif, "", "")
        self.do_test(mods.btc_wif, "", "")
        self.do_test(mods.btc_wif, "", "")
        self.do_test(mods.btc_wif, "", "")

class TestETHChecksum(ModTest):
    def test(self):
        self.do_test(mods.eth_checksum, "", "")
        self.do_test(mods.eth_checksum, "", "")
        self.do_test(mods.eth_checksum, "", "")
        self.do_test(mods.eth_checksum, "", "")
        self.do_test(mods.eth_checksum, "", "")

class TestETHAddress(ModTest):
    def test(self):
        self.do_test(mods.eth_address, "", "")
        self.do_test(mods.eth_address, "", "")
        self.do_test(mods.eth_address, "", "")
        self.do_test(mods.eth_address, "", "")
        self.do_test(mods.eth_address, "", "")
