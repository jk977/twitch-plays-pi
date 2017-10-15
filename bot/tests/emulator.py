# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/emulator.py
# Compiled at: 2017-10-14 16:36:37
# Size of source mod 2**32: 967 bytes
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