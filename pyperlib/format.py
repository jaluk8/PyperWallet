from pyperlib import data
from functools import reduce
import math


class CombinationError(Exception):
    """Raise when combining two uncompatible formats."""


class Format:
    """Represent a data format, such as wif or addresses."""

    def __init__(self, name, data_type, length=[],
                 prefix=[], suffix=[], cryptor=None):
        """Create a new format with certain requirements."""

        if type(prefix) is not list:
            prefix = [prefix]
        if type(suffix) is not list:
            suffix = [suffix]
        if type(length) is not list:
            length = [length]

        prefix = [data.HexData(p) for p in prefix]
        suffix = [data.HexData(s) for s in suffix]

        self.name = name
        self.data_type = data_type
        self.length = length
        self.prefix = prefix
        self.suffix = suffix
        self.cryptor = cryptor

    def match(self, d):
        """Return whether data d matches the rules of this format."""

        if type(d) is str:
            try:
                d = self.data_type(d)
            except Exception:
                return False

        if len(d) not in self.length:
            return False

        if len(self.prefix) > 0:
            prefix_match = False

            for pre in self.prefix:
                pre_len = len(pre)
                prefix = d[:pre_len]
                if prefix == pre:
                    prefix_match = True

            if not prefix_match:
                return False

        if len(self.suffix) > 0:
            suffix_match = False

            for suf in self.suffix:
                suf_len = len(suf)
                suffix = d[-suf_len:]
                if suffix == suf:
                    suffix_match = True

            if not suffix_match:
                return False

        return True


class CombinedFormat:
    """A format that is the union of multiple other formats."""

    def __init__(self, *formats):
        """Create the format from a list of formats with a joined name."""
        self.name = formats[0].name
        self.data_type = formats[0].data_type
        self.formats = formats
        self.cryptor = None

        for f in formats:
            if f.name != self.name or f.data_type != self.data_type:
                raise CombinationError("formats are not compatible")

    def match(self, d):
        """Return the union of all format matches."""

        def union(f1, f2):
            """Return the union of two format matches."""
            if type(f1) is bool:
                return f1 or f2.match(d)
            else:
                return f1.match(d) or f2.match(d)

        return reduce(union, self.formats)


class NoFormat:
    """A blank format interface, the format equivalent of None."""

    def __init__(self):
        """Initialize a blank format."""
        self.name = "none"

    def match(self, d):
        """This format matches nothing."""
        return False


class AutoDetector:
    """Automatically detect formats for given data."""

    def __init__(self, formats, prompt=None):
        """Create the detector with a list of formats."""

        self.formats = formats
        self.prompt = prompt

    def detect(self, d):
        """Run detection on a piece of data."""

        valid = [f for f in self.formats if f.match(d)]

        if len(valid) == 0:
            return None
        elif len(valid) == 1:
            return valid[0]
        else:
            desc = "The format for " + str(d) + " could not be auto-detected."
            opts = [f.name for f in valid]
            name = self.prompt.prompt_list("Format", desc=desc, options=opts)

            valid = [f for f in valid if f.name == name]
            return valid[0]
