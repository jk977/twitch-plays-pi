# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/dummies.py
# Compiled at: 2017-10-13 23:57:39
# Size of source mod 2**32: 1687 bytes
import unittest
from tests.structs.dummychat import DummyChat
from tests.structs.dummyinput import DummyInput
from tests.structs.dummyemu import DummyEmu

class TestChat(unittest.TestCase):

    def setUp(self):
        self.chat = DummyChat()

    def test_send(self):
        message = 'Hiya!'
        self.assertEqual(message, self.chat.send_message(message), 'Chat send failed.')

    def test_get(self):
        self.assertEqual(self.chat.message, self.chat.get_message(), 'Chat get failed.')

    def test_close(self):
        self.assertTrue(self.chat.close(), 'Chat close failed.')


class TestInput(unittest.TestCase):

    def setUp(self):
        self.input = DummyInput('down', 6)

    def test_validate(self):
        fail_msg = 'Input validate failed'
        self.assertTrue(DummyInput.validate('right*9'), fail_msg)
        self.assertTrue(DummyInput.validate('right9'), fail_msg)
        self.assertTrue(DummyInput.validate('right'), fail_msg)
        self.assertFalse(DummyInput.validate('9*wrong'), fail_msg)

    def test_serialize(self):
        self.assertEqual(self.input.serialize(), 'down*6', 'Input serialize failed.')

    def test_deserialize(self):
        fail_msg = 'Input deserialize failed.'
        other = DummyInput.deserialize('down*6')
        other2 = DummyInput.deserialize('down6')
        self.assertEqual(other, self.input, fail_msg)
        self.assertEqual(other2, self.input, fail_msg)


class TestEmulator(unittest.TestCase):

    def test_send(self):
        test_input = 'down6'
        self.assertEqual(test_input, DummyEmu.send_input(test_input), 'Emulator send failed.')


if __name__ == '__main__':
    unittest.main()