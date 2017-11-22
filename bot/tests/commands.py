import unittest

from chat.commands.commandlist import CommandList
from chat.command import Command
from tests.structs.dummychat import DummyChat

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.chat = DummyChat()

    def test_get(self):
        command = CommandList.get('help', self.chat, 'message')
        self.assertTrue(command and isinstance(command, Command), 'Command get failed')

    def test_validate(self):
        fail_msg = 'Command validate failed'

        self.assertTrue(CommandList.validate('help'), fail_msg)
        self.assertTrue(CommandList.validate('!help'), fail_msg)
        self.assertTrue(CommandList.validate('song'), fail_msg)
        self.assertTrue(CommandList.validate('!song'), fail_msg)
        self.assertTrue(CommandList.validate('restart'), fail_msg)
        self.assertTrue(CommandList.validate('!restart'), fail_msg)
        self.assertFalse(CommandList.validate('not a function'), fail_msg)
        self.assertFalse(CommandList.validate('!not a function'), fail_msg)