from pyperlib import format, data
from unittest import TestCase


formats = [
    format.Format("btc_addr", data.Base58Data, min_len=25, max_len=25,
                  prefix="00"),
    format.Format("btc_wif", data.Base58Data, min_len=37, max_len=38,
                  prefix="80"),
    format.Format("priv", data.HexData, min_len=32, max_len=32),
    format.Format("eth_addr", data.StringData, min_len=42, max_len=42,
                  prefix="3078")
    ]

examples = {
    "KyF4khaPVK9YeMBUukyKwq5qKvYNux4KM2FibQ7bZWxTaYVTn6XU": "btc_wif",
    "5JNrhoR2HJ1fH5ts1n2D77o35MrWCEj3gQvBWTc3oZi55uuMu34": "btc_wif",
    "1PYqAUK4q8Lbq32o32ouyQMUFkzszw7ywx": "btc_addr",
    "ab2aeb09578892b1658ee824ae166772c57ce4b77685eca3ea6647da84b96287": "priv",
    "0xB8F758b3f2016Bb391fb18C7Ef39847ef164649e": "eth_addr"
    }


class TestFormat(TestCase):
    """Test whether if common formats are correctly identified."""

    def do_test(self, result, string):
        """Assert that string is identified as result."""
        for f in formats:
            c1 = f.match(string)
            c2 = result == f.name
            self.assertEqual(c1, c2)

    def test_all(self):
        """Run do_test with all formats."""

        for string, result in examples.items():
            self.do_test(result, string)


class TestAutoDetect(TestCase):
    """Test whether the autodetector works."""

    def test_all(self):
        """Create an autodetector and run it on examples."""
        ad = format.AutoDetector(formats)

        for string, result in examples.items():
            actual = ad.detect(string).name
            self.assertEqual(actual, result)
