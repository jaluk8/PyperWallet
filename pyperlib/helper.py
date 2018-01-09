from unittest import TestCase
from unittest.mock import patch


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


class CliTestCase(TestCase):
    """A testcase that involves stdin or stdout."""

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
                return f(**kwargs)
        elif stdin is None:
            with patch('builtins.print', new_callable=self.mock_print):
                result = f(**kwargs)
                self.assertEqual(self.out, stdout)
                return result
        else:
            return f(**kwargs)
