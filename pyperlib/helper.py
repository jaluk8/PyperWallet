from unittest import TestCase
from unittest.mock import patch


class NameFactory:
    """Create a class from a name."""

    suffix = ""
    caps = True
    initialized = False

    def __init__(self):
        """A NameFactory is not an object."""
        raise NotImplementedError("A NameFactory object shouldn't be created.")

    @classmethod
    def append_name(cls, name):
        """Return the class name from a user-readable name."""
        if name[:4].lower() == "base":
            return None

        if cls.caps:
            name = name.title()

        return name + cls.suffix

    @classmethod
    def get(cls, name):
        """Return the proper type, if it exists."""
        cls.try_init()
        name = cls.append_name(name)

        if name in cls.pool:
            return cls.pool[name]
        else:
            return None

    @classmethod
    def has(cls, name):
        """Return whether the type exists."""
        cls.try_init()
        name = cls.append_name(name)

        return name in cls.pool

    @classmethod
    def list(cls):
        """List all valid names that can be passed into get."""
        cls.try_init()
        names = []
        for var in cls.pool:
            if var.endswith(cls.suffix):
                suf_len = len(cls.suffix)
                if suf_len > 0:
                    name = var[:-suf_len]
                else:
                    name = var
                name = name.lower()
                if name[:4] != "base":
                    names.append(name)
        names.sort()
        return names

    @classmethod
    def dict(cls):
        """Return a dict of valid names and objects."""
        cls.try_init()
        names = cls.list()
        d = {}
        for name in names:
            d[name] = cls.get(name)
        return d

    @classmethod
    def try_init(cls):
        """Run init if it has not already been run."""
        if not cls.initialized:
            cls.init()
            cls.initialized = True

    @classmethod
    def init(cls):
        """By default, no initialization is needed."""


class TestNameFactory(TestCase):
    """A TestCase for the NameFactory class."""

    factory = None

    def do_test(self, name, i):
        """Check that you get i when looking for name."""
        self.assertEqual(self.factory.get(name), i)

    def test_list(self):
        """Get a list of all names and check for correctness."""
        for name in self.factory.list():
            obj = self.factory.get(name)
            self.assertNotEqual(obj, None)


class CliTestCase(TestCase):
    """A testcase that involves stdin or stdout."""

    maxDiff = None

    def mock_print(self):
        """Creates the mock print function."""
        def print(x):
            """Record the input in self.out."""
            self.out += x + "\n"
        return print

    def cli_test(self, f, stdin=None, stdout=None, **kwargs):
        """Run test function f with some inport and/or output."""
        self.out = ""

        if stdout is None:
            with patch("builtins.input", side_effect=stdin):
                with patch('builtins.print', new_callable=self.mock_print):
                    return f(**kwargs)
        elif stdin is None:
            with patch('builtins.print', new_callable=self.mock_print):
                result = f(**kwargs)
                self.assertEqual(self.out, stdout)
                return result
        else:
            return f(**kwargs)
