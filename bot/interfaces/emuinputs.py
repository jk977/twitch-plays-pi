from . import *
from interfaces.validator import Validator

class EmuInputs(Validator):
    """
    Base class for type-safe containers containing EmuInput children classes.
    Note that there isn't one for Cheat objects; this restricts cheats to 1 per message
    and prevents cheats from being mixed with buttons.
    """

    @abstractproperty
    def destination(self):
        pass

    @abstractproperty
    def inputs(self):
        pass