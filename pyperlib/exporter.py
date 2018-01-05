class BaseExporter:
    """Takes in a Coin object and exports it to python values."""

    def __init__(self):
        """Exporters require no initialization."""
        pass

    def run(self, c):
        """Exports the given coin to three python strings."""
        wif = None
        view = None
        addr = None

        if c.wif is not None:
            wif = c.wif_string()

        if c.view is not None:
            view = c.view_string()

        if c.addr is not None:
            addr = c.addr_string()

        return wif, view, addr
