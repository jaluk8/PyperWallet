#!/usr/bin/env python3

from pyperlib import walletgen
from pathlib import Path

path = str(Path(__file__).parent.absolute())

for name in walletgen.DesignerFactory.list():
    Designer = walletgen.DesignerFactory.get(name)
    d = Designer(path)
    d.run()
