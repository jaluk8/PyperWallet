#!/usr/bin/env python3

from pyperlib.wallet import cliwallet
import sys

w = cliwallet.CliWallet(sys.argv)

try:
    w.run()
except KeyboardInterrupt:
    sys.exit(3)
