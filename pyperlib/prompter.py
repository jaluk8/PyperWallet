from getpass import getpass


class BasePrompter:
    """The base interface for prompters, which grab info from the user."""

    @classmethod
    def prompt_info(cls, name, type_f=None, options=None):
        """Prompts the user for a normal piece of information."""
        raise NotImplementedError("Prompter does not support info prompts.")

    @classmethod
    def prompt_pass(cls, name, type_f=None, repeat=True):
        """Prompts the user for secret information, like a password."""
        raise NotImplementedError("Prompter does not support pass prompts.")


class CliPrompter:
    """Grab info from the user using stdin."""

    pass_input = getpass

    @classmethod
    def try_to_cast(cls, i, type_f):
        """Return i casted as type_f, or None if impossible."""
        if type_f is None:
            return i
        else:
            try:
                return type_f(i)
            except Exception:
                print("Incorrect type.")
                return None

    @classmethod
    def prompt_info(cls, name, type_f=None, options=None):
        """Prompts the user for a normal piece of information."""
        info = None

        option_str = ""
        if options is not None:
            option_str = " ("
            option_str += "/".join(options)
            option_str += ")"

        prompt_str = name + option_str + ": "

        while info is None:
            i = input(prompt_str)

            if options is not None and i not in options:
                print("That is not one of the available options.")
                continue

            info = cls.try_to_cast(i, type_f)

        return info

    @classmethod
    def prompt_pass(cls, name, type_f=None, repeat=True):
        """Prompts the user for secret information, like a password."""
        info = None

        while info is None:
            i1 = cls.pass_input(name + " (will not echo): ")
            if repeat:
                i2 = cls.pass_input(name + " (confirm): ")
            else:
                i2 = i1

            if i1 != i2:
                print(name + " does not match.")
                continue

            info = cls.try_to_cast(i1, type_f)

        return info
