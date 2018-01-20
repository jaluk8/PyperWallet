#!/usr/bin/env python3

from pyperlib import prompter
from pyperlib.wallet import guiwallet
import sys

w = guiwallet.GuiWallet(sys.argv)

try:
    w.run()
except KeyboardInterrupt:
    sys.exit(3)
