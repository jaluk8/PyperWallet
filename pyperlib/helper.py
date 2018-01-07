from unittest import TestCase


class NameFactory:
    """Create a class from a name."""

    suffix = ""

    @classmethod
    def get(cls, name):
        """Returns the proper type, if it exists."""
        if name[:4].lower() == "base":
            return None

        name = name.title() + cls.suffix

        if name in cls.pool:
            return cls.pool[name]
        else:
            return None

class TestNameFactory(TestCase):
    """A TestCase for the NameFactory class."""

    factory = None

    def do_test(self, name, i):
        """Check that you get i when looking for name."""
        self.assertEqual(self.factory.get(name), i)
