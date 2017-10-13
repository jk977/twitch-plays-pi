import os
from interfaces.emulator import Emulator
from interfaces.emuinput import EmuInput

class NES(Emulator):
    def send_input(emu_input):
        if not isinstance(emu_input, EmuInput):
            raise TypeError('Input must be an EmuInput object.')
        elif not os.access(emu_input.destination, os.W_OK):
            raise PermissionError('Input destination is not writable.')
        
        with open(emu_input.destination, 'w') as file:
            file.write(emu_input.serialize())