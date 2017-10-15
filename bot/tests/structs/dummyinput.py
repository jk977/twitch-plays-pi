from numbers import Number
from interfaces.emuinput import EmuInput

class DummyInput(EmuInput):
    """
    Dummy class for use in unit testing.
    """
    def _validate_content(content):
        return True

    def _validate_count(count):
        return isinstance(count, Number)