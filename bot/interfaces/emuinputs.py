# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/interfaces/emuinputs.py
# Compiled at: 2017-10-14 19:19:47
# Size of source mod 2**32: 444 bytes
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