from getpass import getpass


class BasePrompter:
    """The base interface for prompters, which grab info from the user."""

    def prompt_info(self, name, desc="", type_f=None):
        """Prompt the user for a normal piece of information."""
        raise NotImplementedError("Prompter does not support info prompts.")

    def prompt_list(self, name, desc="", options=[]):
        """Prompt the user to pick an item out of a list of strings."""
        raise NotImplementedError("Prompter does not support list prompts.")

    def prompt_pass(self, name, desc="", type_f=None, repeat=True):
        """Prompt the user for secret information, like a password."""
        raise NotImplementedError("Prompter does not support pass prompts.")


class CliPrompter(BasePrompter):
    """Grab info from the user using stdin."""

    pass_input = getpass

    def try_to_cast(self, i, type_f):
        """Return i casted as type_f, or None if impossible."""
        if type_f is None:
            return i
        else:
            try:
                return type_f(i)
            except Exception:
                print("Incorrect type.")
                return None

    def prompt_info(self, name, desc="", type_f=None):
        """Prompt the user for a normal piece of information."""
        info = None
        prompt_str = name + ": "

        while info is None:
            if desc != "":
                print(desc)
            i = input(prompt_str)

            info = self.try_to_cast(i, type_f)

        return info

    def prompt_list(self, name, desc="", options=[]):
        """Prompt the user to pick an item out of a list of strings."""
        info = None

        while info is None:
            if desc != "":
                print(desc)
            print(name + " options:")
            for i, o in enumerate(options):
                print(" " + str(i+1) + ") " + o)
            i = input("Option number: ")

            num = self.try_to_cast(i, int)
            if num is None:
                print("Please enter a number.")
                continue

            if num < 1 or num > len(options):
                print("That number is not a valid option.")
                continue

            info = options[num - 1]

        return info

    def prompt_pass(self, name, desc="", type_f=None, repeat=True):
        """Prompt the user for secret information, like a password."""
        info = None

        while info is None:
            if desc != "":
                print(desc)
            i1 = self.pass_input(name + " (will not echo): ")
            if repeat:
                i2 = self.pass_input(name + " (confirm): ")
            else:
                i2 = i1

            if i1 != i2:
                print(name + " does not match.")
                continue

            info = self.try_to_cast(i1, type_f)

        return info
