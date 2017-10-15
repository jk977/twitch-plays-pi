# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/structs/dummyemu.py
# Compiled at: 2017-10-11 17:40:06
# Size of source mod 2**32: 172 bytes
from interfaces.emulator import Emulator

class DummyEmu(Emulator):
    """
    Dummy class for use in unit testing.
    """

    def send_input(input):
        return input