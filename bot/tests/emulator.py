import unittest

from nes.emuchoice import EmuChoice
from nes.emulator import NES

class TestEmulator(unittest.TestCase):
    def setUp(self):
        self.buttons = EmuChoice('start*9')
        self.cheat = EmuChoice('attack')

    def test_send(self):
        fail_msg = 'Emulator send failed'
        NES.send_input(self.buttons)
        NES.send_input(self.cheat)

        with open(self.buttons.input.destination, 'r') as file:
            button_contents = file.read()

        with open(self.cheat.input.destination, 'r') as file:
            cheat_contents = file.read()

        self.assertEqual(button_contents, self.buttons.input.serialize(), fail_msg)
        self.assertEqual(cheat_contents, self.cheat.input.serialize(), fail_msg)

        try:
            NES.send_input('not an input')
            self.assertTrue(False, fail_msg)
        except TypeError:
            pass


if __name__ == '__main__':
    unittest.main()