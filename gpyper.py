#!/usr/bin/env python3

from pyperlib import prompter
from pyperlib.wallet import cliwallet
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication([])

w = cliwallet.CliWallet(sys.argv, prompter.GuiPrompter())

try:
    w.run()
except KeyboardInterrupt:
    sys.exit(3)
