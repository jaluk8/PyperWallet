class InvalidCoinError(Exception):
    """An error that is raised when an address checksum fails."""


class Setting:
    """A single user-controllable coin setting."""

    def __init__(self, name, s_type, default, description=None):
        """Create a new setting, given a name and default value."""
        if description is None:
            description = "no description"

        self.description = description
        self.name = name
        self.default = default
        self.s_type = s_type


class CoinSettings:
    """A container for keeping track of user-defined coin settings."""

    settings = [
        Setting("compression", bool, True, "whether to use a compressed \
address or not")
        ]

    def __init__(self, **kwargs):
        """Sets any attributes, either from kwargs or self.settings."""
        for s in self.settings:
            setattr(self, s.name, s.default)
        self.apply(**kwargs)

    def apply(self, **kwargs):
        """Apply a list of arguments to the settings, if not None."""
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

    def get(self, name):
        """Return the setting named name."""
        return getattr(self, name)


class CoinList:
    """A class that can generate a list of Coin classes."""

    @classmethod
    def list(cls):
        """The interface for creating a coin list."""
        return []
