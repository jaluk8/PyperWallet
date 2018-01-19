from getpass import getpass
from PyQt5.QtWidgets import QWidget, QInputDialog, QMessageBox, QLineEdit
import traceback


class BasePrompter:
    """The base interface for prompters, which grab info from the user."""

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
        raise NotImplementedError("Prompter does not support info prompts.")

    def prompt_list(self, name, desc="", options=[]):
        """Prompt the user to pick an item out of a list of strings."""
        raise NotImplementedError("Prompter does not support list prompts.")

    def prompt_pass(self, name, desc="", type_f=None, repeat=True):
        """Prompt the user for secret information, like a password."""
        raise NotImplementedError("Prompter does not support pass prompts.")

    @staticmethod
    def error_type(e):
        """Return a human-readable type of the given error."""
        tpe = str(type(e))
        tpe = tpe[8:-2]
        return tpe

    def show_error(self, e, debug=False):
        """Show an error to the user."""
        raise NotImplementedError("Prompter does not support error showing.")


class CliPrompter(BasePrompter):
    """Grab info from the user using stdin."""

    def pass_input(self, prompt):
        """Securely ask the user for a password."""
        return getpass(prompt=prompt)

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

    def show_error(self, e, debug=False):
        """Show an error in the command line."""
        if debug:
            traceback.print_exc()
        else:
            msg = str(e)
            tpe = self.error_type(e)
            print("Error: " + tpe)
            if msg != "":
                print(msg)


class GuiPrompter(BasePrompter, QWidget):
    """Prompt the user through a qt dialog."""

    def get_text(self, name, prompt, **kwargs):
        """Run an InputDialog to get some text back."""
        return QInputDialog.getText(self, name + ' prompt', prompt, **kwargs)

    def show_text(self, name, text):
        """Use a QMessageBox to show some information to the user."""
        QMessageBox.question(self, name, text, QMessageBox.Ok, QMessageBox.Ok)

    def prompt_info(self, name, desc="", type_f=None):
        """Prompt the user for a normal piece of information."""
        info = None
        prompt_str = name + ":"
        if desc != "":
            prompt_str = desc + "\n" + prompt_str

        while info is None:
            i, ok = self.get_text(name, prompt_str)

            if ok:
                info = self.try_to_cast(i, type_f)

        return info

    def prompt_list(self, name, desc="", options=[]):
        """Prompt the user to pick an item out of a list of strings."""
        info = None

        while info is None:
            if desc != "":
                msg = desc + "\n"
            msg += name + " options:"
            i, ok = QInputDialog.getItem(self, name + " prompt", msg, options,
                                         0, False)

            if ok:
                info = i

        return info

    def prompt_pass(self, name, desc="", type_f=None, repeat=True):
        """Prompt the user for secret information, like a password."""
        info = None
        prompt_str = name + ":"
        if desc != "":
            prompt_str = desc + "\n" + prompt_str
        conf_str = prompt_str[:-1] + " (confirm):"

        while info is None:
            i1, ok = self.get_text(name, prompt_str, echo=QLineEdit.Password)

            if ok:
                if repeat:
                    i2, ok = self.get_text(name, conf_str,
                                           echo=QLineEdit.Password)
                else:
                    i2 = i1

                if ok:
                    if i1 == i2:
                        info = self.try_to_cast(i1, type_f)
                    else:
                        self.show_text(name + " mismatch",
                                       "The two inputs do not match.")
        return info

    def show_error(self, e, debug=False):
        """Show an error to the user."""
        if debug:
            traceback.print_exc()
        tpe = self.error_type(e)
        msg = "Error: " + str(e)
        self.show_text(tpe, msg)
