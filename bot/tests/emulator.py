import unittest
from nes.button import Button
from nes.cheat import Cheat
from nes.emulator import NES

class TestEmulator(unittest.TestCase):
    def setUp(self):
        self.button = Button('down', 5)
        self.cheat = Cheat('attack')

    def test_send(self):
        fail_msg = 'Emulator send failed'

        NES.send_input(self.button)
        NES.send_input(self.cheat)
        
        with open(self.button.destination, 'r') as file:
            button_contents = file.read()
            
        with open(self.cheat.destination, 'r') as file:
            cheat_contents = file.read()
            
        self.assertEqual(button_contents, self.button.serialize(), fail_msg)
        self.assertEqual(cheat_contents, self.cheat.serialize(), fail_msg)
        
        try:
            NES.send_input('not an input')
            self.assertTrue(False, fail_msg)
        except TypeError:
            pass
        
        
if __name__ == '__main__':
    unittest.main()