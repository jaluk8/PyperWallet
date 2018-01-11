#!/usr/bin/env python3

from pyperlib import wallet, prompter
import argparse


description = """\
"""


coin_help = "the ticker name of the coin"


importer_help = "control how the coin is initially created"


exporter_help = "control how the coin will be displayed at the end"


encrypt_help = "encrypt the coin with an encryption standard"


def str2bool(s):
    """A bool constructor that uses strings properly."""
    if s.lower() in ("true", "t", "yes", "y"):
        return True
    elif s.lower() in ("false", "f", "no", "n"):
        return False
    else:
        raise argparse.ArgumentTypeError(s + " is not a boolean")


def make_opt(parser, *args, default=None, descriptions=False, help=None,
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

    parser.add_argument(*args, choices=choices, default=default, help=help,
                        **kwargs)


def make_parser():
    """Create the parser and add all needed arguments."""
    formatter = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter,
                                     description=description)

    coin_f = wallet.Wallet.coin_f
    make_opt(parser, "-c", factory=coin_f, default="btc", metavar="name",
             dest="coin", help=coin_help)

    imp_f = wallet.Wallet.importer_f
    make_opt(parser, "-i", factory=imp_f, default="gen", metavar="input",
             dest="importer", help=importer_help, descriptions=True)

    exp_f = wallet.Wallet.exporter_f
    make_opt(parser, "-o", factory=exp_f, default="cli", metavar="output",
             dest="exporter", help=exporter_help, descriptions=True)

    enc_f = wallet.Wallet.cryptor_f
    make_opt(parser, "-e", factory=enc_f, default="none",
             default_desc="no encryption", metavar="encryption",
             dest="cryptor", help=encrypt_help, descriptions=True)

    for setting in wallet.Wallet.Settings.settings:
        help = setting.description + " (default=" + str(setting.default) + ")"
        arg = "--" + setting.name

        if setting.s_type is bool:
            s_type = str2bool
        else:
            s_type = setting.s_type

        parser.add_argument(arg, default=setting.default, type=s_type,
                            metavar=setting.name, dest=setting.name, help=help)

    return parser


def proc_args(args):
    """Process the arguments and make a wallet from them."""
    Coin = args.coin
    del args.coin

    Importer = args.importer
    del args.importer

    Exporter = args.exporter
    del args.exporter

    Cryptor = args.cryptor
    del args.cryptor

    setting_args = vars(args)

    w = wallet.Wallet(Coin, Importer, Exporter, Prompt=prompter.CliPrompter,
                      Cryptor=Cryptor, **setting_args)
    w.run()


parser = make_parser()
args = parser.parse_args()
proc_args(args)
