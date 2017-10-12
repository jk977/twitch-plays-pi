from interfaces.emulator import Emulator

class DummyEmu(Emulator):
    '''
    Dummy class for use in unit testing.
    '''
    def send_input(input):
        return input