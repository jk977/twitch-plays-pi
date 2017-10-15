import unittest
from nes.choice import EmuChoice
from nes.emulator import NES

class TestEmulator(unittest.TestCase):

    def setUp(self):
        self.buttons = EmuChoice('start*9')
        self.cheat = EmuChoice('attack')

    def test_send(self):
        fail_msg = 'Emulator send failed'
        NES.send_input(self.buttons)
        NES.send_input(self.cheat)
        with open(self.buttons.destination, 'r') as file:
            button_contents = file.read()
        with open(self.cheat.destination, 'r') as file:
            cheat_contents = file.read()
        self.assertEqual(button_contents, self.buttons.serialize(), fail_msg)
        self.assertEqual(cheat_contents, self.cheat.serialize(), fail_msg)
        try:
            NES.send_input('not an input')
            self.assertTrue(False, fail_msg)
        except TypeError:
            pass


if __name__ == '__main__':
    unittest.main()