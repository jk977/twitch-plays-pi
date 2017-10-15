# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/nes/button.py
# Compiled at: 2017-10-14 19:34:10
# Size of source mod 2**32: 664 bytes
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
        if result == 'a' or result == 'b':
            return result.upper()
        return result

    def _validate_count(count):
        return isinstance(count, Number)

    def _validate_content(content):
        return content.lower() in ('a', 'b', 'start', 'select', 'up', 'down', 'left',
                                   'right')