from pyperlib import data
import math


class Format:
    """Represent a data format, such as wif or addresses."""

    def __init__(self, name, data_type, min_len=0, max_len=math.inf,
                 prefix=None, suffix=None):
        """Create a new format with certain requirements."""

        if type(prefix) is str:
            prefix = data.HexData(prefix)

        if type(suffix) is str:
            suffix = data.HexData(suffix)

        self.name = name
        self.data_type = data_type
        self.min_len = min_len
        self.max_len = max_len
        self.prefix = prefix
        self.suffix = suffix

    def match(self, d):
        """Return whether data d matches the rules of this format."""

        if type(d) is str:
            try:
                d = self.data_type(d)
            except Exception:
                return False

        if len(d) < self.min_len:
            return False

        if len(d) > self.max_len:
            return False

        if self.prefix is not None:
            pre_len = len(self.prefix)
            prefix = d[:pre_len]
            if prefix != self.prefix:
                return False

        if self.suffix is not None:
            suf_len = len(self.suffix)
            suffix = d[-suf_len:]
            if suffix != self.suffix:
                print(self.suffix)
                return False

        return True


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
