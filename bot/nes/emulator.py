from interfaces.emulator import Emulator
from nes.emuchoice import EmuChoice

class NES(Emulator):
    def send_input(choice):
        if not isinstance(choice, EmuChoice):
            raise TypeError('Input must be an EmuChoice object.')

        vote = choice.input

        with open(vote.destination, 'w') as file:
            file.write(vote.serialize())