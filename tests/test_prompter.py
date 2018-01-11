from pyperlib import prompter, helper
from unittest import TestCase


class TestBasePrompter(TestCase):
    """Test that the base prompter interface works."""

    prompt = prompter.BasePrompter

    def do_test(self, f, output=None, error=None, **kwargs):
        """Run f with kwargs and verify output or error is given."""

        if error is None:
            o = f(**kwargs)
            self.assertEqual(o, output)
        else:
            self.assertRaises(error, f, **kwargs)

    def test_all(self):
        """Test that all function return NotImplementedErrors."""

        self.do_test(self.prompt.prompt_info, error=NotImplementedError,
                     name="", type_f=str)
        self.do_test(self.prompt.prompt_list, error=NotImplementedError,
                     name="", options=[])
        self.do_test(self.prompt.prompt_pass, error=NotImplementedError,
                     name="", type_f=str, repeat=True)


class TestCliPrompter(TestBasePrompter, helper.CliTestCase):
    """Test that the cli prompter interface works."""

    prompt = prompter.CliPrompter

    stdin = ["value", "2", "value", "value"]

    def prompt_all(self, name, result):
        """Prompt for name using all prompt functions, expecting a result."""
        pi = self.prompt.pass_input
        self.prompt.pass_input = input

        self.do_test(self.prompt.prompt_info, output=result, name=name)
        self.do_test(self.prompt.prompt_list, output=result, name=name,
                     options=["low", result, "high"])
        self.do_test(self.prompt.prompt_pass, output=result, name=name)

        self.prompt.pass_input = pi

    def test_all(self):
        """Test that stdin and stdout matches the interface."""
        self.cli_test(self.prompt_all, stdin=self.stdin, name="Query",
                      result="value")
