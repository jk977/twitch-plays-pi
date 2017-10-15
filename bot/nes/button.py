import os
from interfaces.emuinput import EmuInput
from numbers import Number

class Button(EmuInput):
    destination = os.path.join(EmuInput.path, 'inputs.txt')

    @classmethod
    def _parse_content(cls, message):
        """
        Overrides parent method to accomodate for FCEUX Lua interface button format.
        """
        result = super()._parse_content(message)
        return result.upper() if (result == 'a' or result == 'b') else result

    def _validate_count(count):
        return isinstance(count, Number)

    def _validate_content(content):
        return content.lower() in ('a', 'b', 'start', 'select', 'up', 'down', 'left', 'right')