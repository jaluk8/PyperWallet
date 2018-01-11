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
        for key, value in kwargs.items():
            setattr(self, key, value)
