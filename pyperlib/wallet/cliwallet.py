from pyperlib import wallet, prompter
import argparse
import sys


description = """\
"""


coin_help = "the name of the coin"
importer_help = "control how the coin is initially created"
exporter_help = "control how the coin will be displayed at the end"
file_help = "the coin will be exported to this file (default=none)."
encrypt_help = "encrypt the coin with an encryption standard"
debug_help = "turn on debugging mode (errors will be shown more verbosely)."


class CliWallet(wallet.Wallet):
    """Create a command line interface for the wallet."""

    def __init__(self, args, prompt=prompter.CliPrompter()):
        """Create the cli from a list of command line arguments."""
        self.make_parser(args[0])
        self.prompt = prompt
        self.args = self.parser.parse_args(args[1:])

    def run(self):
        """Run the wallet."""
        self.proc_args()

    @staticmethod
    def str2bool(s):
        """A bool constructor that uses strings properly."""
        if s.lower() in ("true", "t", "yes", "y"):
            return True
        elif s.lower() in ("false", "f", "no", "n"):
            return False
        else:
            raise argparse.ArgumentTypeError(s + " is not a boolean")

    def make_opt(self, *args, default=None, descriptions=False, help=None,
                 factory=None, default_desc="no description", **kwargs):
        """Create an argument in parser with a nice-looking help string."""
        help += " (default=" + default + "):"

        choices = factory.list()
        if default not in choices:
            choices = [default] + choices

        if descriptions:
            d = factory.dict()
            for name in choices:
                if name in d:
                    desc = d[name].description
                else:
                    desc = default_desc
                help += "\n - " + name + ": " + desc
        else:
            help += " "
            for name in choices:
                help += name + ", "
            help = help[:-2]

        self.parser.add_argument(*args, choices=choices, default=default,
                                 help=help, **kwargs)

    def make_parser(self, prog):
        """Create the parser and add all needed arguments."""
        formatter = argparse.RawTextHelpFormatter
        self.parser = argparse.ArgumentParser(prog=prog,
                                              formatter_class=formatter,
                                              description=description)

        coin_f = self.coin_f
        self.make_opt("-c", factory=coin_f, default="bitcoin", metavar="name",
                      dest="coin", help=coin_help)

        imp_f = self.importer_f
        self.make_opt("-i", factory=imp_f, default="gen", metavar="input",
                      dest="importer", help=importer_help, descriptions=True)

        exp_f = self.exporter_f
        self.make_opt("-o", factory=exp_f, default="text", metavar="output",
                      dest="exporter", help=exporter_help, descriptions=True)

        self.parser.add_argument("-f", default="-", help=file_help,
                                 metavar="file", dest="out_file")

        enc_f = self.cryptor_f
        self.make_opt("-e", factory=enc_f, default="none",
                      default_desc="no encryption", metavar="encryption",
                      dest="cryptor", help=encrypt_help, descriptions=True)

        for setting in self.Settings.settings:
            help = (setting.description + " (default=" +
                    str(setting.default) + ")")
            arg = "--" + setting.name

            if setting.s_type is bool:
                s_type = self.str2bool
            else:
                s_type = setting.s_type

            self.parser.add_argument(arg, default=None, type=s_type,
                                     metavar=setting.name, dest=setting.name,
                                     help=help)

        self.parser.add_argument("--debug", dest="debug", help=debug_help,
                                 action="store_true")

    def proc_args(self):
        """Process the arguments and make a wallet from them."""
        debug = self.args.debug
        del self.args.debug

        Coin = self.args.coin
        del self.args.coin

        Importer = self.args.importer
        del self.args.importer

        Exporter = self.args.exporter
        del self.args.exporter

        out_file = self.args.out_file
        del self.args.out_file
        if out_file in ["-", "none"]:
            out_file = None
        else:
            out_file = open(out_file, "w")

        Cryptor = self.args.cryptor
        del self.args.cryptor

        setting_args = vars(self.args)

        try:
            self.Coin = Coin
            self.Importer = Importer
            self.Exporter = Exporter
            self.Cryptor = Cryptor
            self.out_file = out_file
            self.debug = debug
            self.kwargs = setting_args

            super().run()
        except Exception as e:
            self.prompt.show_error(e, debug)
            sys.exit(1)
