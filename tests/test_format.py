from pyperlib import format, data
from unittest import TestCase


formats = [
    format.Format("btc_addr", data.Base58Data, length=25,
                  prefix="00"),
    format.Format("btc_wif", data.Base58Data, length=[37, 38],
                  prefix="80"),
    format.Format("priv", data.HexData, length=32),
    format.Format("eth_addr", data.StringData, length=42,
                  prefix="3078")
    ]

examples = {
    "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU": "btc_wif",
    "5JNrhoR2HJ1fH5ts1n2D77o35MrWCEj3gQvBWTc3oZi55uuMu34": "btc_wif",
    "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx": "btc_addr",
    "ab2aeb09578892b1658ee824ae166772c57ce4b77685eca3ea6647da84b96287": "priv",
    "0xB8F758b3f2016Bb391fb18C7Ef39847ef164649e": "eth_addr"
    }


pub_examples = {
    "03A8FBD94B07E5C67B3D5FD3432FF892F54DEFF700E9044E21404EBCA42AAE9E7C": "pb",
    "04A8FBD94B07E5C67B3D5FD3432FF892F54DEFF700E9044E21404EBCA42AAE9E7CA74C34F"
    "A16D8B8A202A03FDE8552A24E7F9F3ABF134F0F2B46E07B373833BE27": "pb"
    }


class TestFormat(TestCase):
    """Test whether if common formats are correctly identified."""

    def do_test(self, result, string, formats):
        """Assert that string is identified as result."""
        for f in formats:
            c1 = f.match(string)
            c2 = result == f.name
            self.assertEqual(c1, c2)

    def test_all(self, examples=examples, formats=formats):
        """Run do_test with all formats."""

        for string, result in examples.items():
            self.do_test(result, string, formats)


class TestCombinedFormat(TestFormat):
    """Test whether combining multiple formats works."""

    def monkey(self, i1, i2):
        """Assert that combining formats of the given indices does not work."""
        self.assertRaises(format.CombinationError, format.CombinedFormat,
                          formats[i1], formats[i2])

    def test_all(self):
        """Run do_test with combined formats and do some monkey testing."""
        for i in range(len(formats)):
            for j in range(i+1, len(formats)):
                self.monkey(i, j)

        pub_u = format.Format("pb", data.HexData, length=33,
                              prefix=["02", "03"])
        pub_c = format.Format("pb", data.HexData, length=65, prefix="04")
        pub_format = format.CombinedFormat(pub_u, pub_c)

        formats2 = formats + [pub_format]
        examples2 = examples.copy()
        examples2.update(pub_examples)

        super().test_all(examples2, formats2)


class TestAutoDetect(TestCase):
    """Test whether the autodetector works."""

    def test_all(self):
        """Create an autodetector and run it on examples."""
        ad = format.AutoDetector(formats)

        for string, result in examples.items():
            actual = ad.detect(string).name
            self.assertEqual(actual, result)
