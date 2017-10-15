# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/nes/emulator.py
# Compiled at: 2017-10-14 19:37:22
# Size of source mod 2**32: 522 bytes
import os
from interfaces.emulator import Emulator
from nes.choice import EmuChoice

class NES(Emulator):

    def send_input(choice):
        if not isinstance(choice, EmuChoice):
            raise TypeError('Input must be an EmuChoice object.')
        destination = choice.destination
        if not os.access(destination, os.W_OK):
            raise PermissionError('Input destination "{}" is not writable.'.format(destination))
        with open(destination, 'w') as file:
            file.write(choice.serialize())