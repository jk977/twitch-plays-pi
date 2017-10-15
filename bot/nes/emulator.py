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