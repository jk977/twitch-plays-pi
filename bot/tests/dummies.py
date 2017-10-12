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
        self.assertTrue(DummyInput.validate('9*right'), fail_msg)
        self.assertFalse(DummyInput.validate('wrong*9'), fail_msg)

    def test_serialize(self):
        self.assertEqual(self.input.serialize(), '6*down', 'Input serialize failed.')

    def test_deserialize(self):
        other = DummyInput.deserialize('6*down')
        self.assertEqual(other, self.input, 'Input deserialize failed.')


class TestEmulator(unittest.TestCase):
    def test_send(self):
        test_input = '6down'
        self.assertEqual(test_input, DummyEmu.send_input(test_input), 'Emulator send failed.')


if __name__ == '__main__':
    unittest.main()