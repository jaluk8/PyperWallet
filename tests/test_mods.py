from unittest import TestCase
from pyperlib import mods, data


class ModTest(TestCase):
    """A TestCase base class for any mods."""

    def do_test(self, mod, o, *a):
        """Run the mod given *a, and expect o."""
        args = [data.HexData(i) for i in a]
        self.assertEqual(mod(*args), data.HexData(o))


class TestSha256(ModTest):
    """A TestCase for the Sha256 Mod."""

    def test(self):
        """Use do_test to check sha256."""
        self.do_test(
            mods.Sha256,
            "995DA3CF545787D65F9CED52674E92EE8171C87C7A4008AA4349EC47D21609A7",
            "ABCDEF")
        self.do_test(
            mods.Sha256,
            "D2BDEC3101EB836B1A87AFBC37E20AAFBBD9C77D2E146DDA4C732D44C0BF4515",
            "00AB")
        self.do_test(
            mods.Sha256,
            "8F414150ACB8F255A847C933BEB781B6B3552D502032A5F5A1374F1D2D00B877",
            "ACD300")


class TestRipeMD160(ModTest):
    """A TestCase for the RipeMD160 Mod."""

    def test(self):
        """Use do_test to check ripemd160."""
        self.do_test(mods.Ripemd160,
                     "A3335A6EE4A6DA99932AEEE33423DD9AFE8623D7", "ABCDEF")
        self.do_test(mods.Ripemd160,
                     "F6D37D7E7D1743BD8623D32645932CB840F858DA", "00AB")
        self.do_test(mods.Ripemd160,
                     "D1A3258B5F6EB32A452BC6F3253ABC65C0275CF6", "ACD300")


class TestConcat(ModTest):
    """A TestCase for the Concat Mod."""

    def test(self):
        """Use do_test to check concat."""
        self.do_test(mods.Concat, "A53E", "A5", "3E")
        self.do_test(mods.Concat, "0000AE45", "0000", "AE45")
        self.do_test(mods.Concat, "A3", "", "A3")
        self.do_test(mods.Concat, "00001F4E", "00", "001F4E")
        self.do_test(mods.Concat, "1F00", "1F", "00")


class TestXor(ModTest):
    """A TestCase for the Xor Mod."""

    def test(self):
        """Use do_test to check xor."""
        self.do_test(mods.Xor, "01", "00", "01")
        self.do_test(mods.Xor, "00", "01", "01")
        self.do_test(mods.Xor, "E8EC", "4321", "ABCD")
        self.do_test(mods.Xor, "0012", "0a10", "0a02")
        self.do_test(mods.Xor, "00A3", "0000", "00A3")


class TestSlice(ModTest):
    """A TestCase for the Slice Mod."""

    def slice_undo(self, i):
        """Slice i in half, concat it together, and check."""
        d = data.HexData(i)
        d1 = mods.Slice(d, 0, 2)
        d2 = mods.Slice(d, 2, 4)
        dc = mods.Concat(d1, d2)
        self.assertEqual(d, dc)

    def test(self):
        """Run slice_undo on various Data."""
        self.slice_undo("00112233")
        self.slice_undo("00000000")
        self.slice_undo("A64FEC23")
        self.slice_undo("00AE3400")


class TestScrypt(ModTest):
    """A TestCase for the Scrypt Mod."""

    def scrypt(self, key, password, salt):
        """Run scrypt on password and salt, expect key."""
        salt = data.HexData(salt)
        key = data.HexData(key)
        password = data.StringData(password, "utf-8", "NFC")
        self.assertEqual(key, mods.Scrypt(password, salt))

    def test(self):
        """Check example data with self.scrypt."""
        self.scrypt("35A47442A15AB515B469C9647F62A0C761B26AE02A5C5CE074BDDB62A"
                    "231D7FD600C845477728149934871DE29D8AF2493F4446ED2F586BAEC"
                    "B8E58185AACFB8", "Hello", "00")
        self.scrypt("5C4737E7A3632E3E04D550407E76F957EF3377D65C4ABEE225C6C3DE5"
                    "FEFD7E5F38C5BF1447324148CA36D1B91B146D851A01BCC54FBC631EE"
                    "0CB19B3865BEEF", "TheTestHere", "0011AAFF")
        self.scrypt("F5C45C41E6D91985316117D1FF16CC815D05A7F7A1CB045944FB0A04F"
                    "EA1F2FF2955468C9B4069C5468D4FE1541CD8CFD230B6575449D1AD91"
                    "A920C331E80E2F", "Password", "FA356E00")


class TestAes256(ModTest):
    """A TestCase for the Aes256 Mods."""

    def do_test(self, o, i, k):
        """Encrypt i into o and decrypt o into i with k."""
        o = data.HexData(o)
        i = data.HexData(i)
        k = data.HexData(k)

        enc = mods.Aes256Enc(i, k)
        dec = mods.Aes256Dec(o, k)

        self.assertEqual(enc, o)
        self.assertEqual(dec, i)

    def test(self):
        """Run do_test on example data."""
        self.do_test("AF7A445C1915E6A246229EE3C8B202A7AF7A445C1915E6A246229EE3"
                     "C8B202A7",
                     "5C4737E7A3632E3E5C4737E7A3632E3E5C4737E7A3632E3E5C4737E7"
                     "A3632E3E",
                     "5C4737E7A3632E3E5C4737E7A3632E3E")
        self.do_test("736CA8C2AAAD7B2A461FA9BC9DC606D6FFE1A35A765E36F8C581ECE5"
                     "590E6087",
                     "000037E7A3632E3E5C4737E7A3632E3E5C4737E7A3632E3E5C4737E7"
                     "A3632E3E",
                     "000000E7A3632E3E5C4737E7A3632E3E")
        self.do_test("3829BC045E212560248DB7D1E2621D009039F67427135D7AF75DC6AC"
                     "75DD8058",
                     "5C4737E7A3632E3E5C4737E7A3632E3E5C4737E7A3632E3E5C4737E7"
                     "A3000000",
                     "5C4737E7A3632E3E5C4737E7A3630000")


class TestKeccak(ModTest):
    """A TestCase for the Keccak Mod."""

    def test(self):
        """Check keccak hashes of some Data."""
        self.do_test(mods.Keccak,
                     "54A8C0AB653C15BFB48B47FD011BA2B9617AF01CB45CAB344ACD57C9"
                     "24D56798", "0000")
        self.do_test(mods.Keccak, "7A9708896A15EF140A04B38B9414EF409B5C3196E7C"
                     "60B479F80E48C302F0ADD", "A4B387A200")
        self.do_test(mods.Keccak, "FDA66FC2D882FF395D5DC2955E833B8F1E5FCC96907"
                     "E0B50B11C1EB4349F522F", "A57E98D0")
