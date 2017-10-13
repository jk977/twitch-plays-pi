import unittest
from chat.commands.commandlist import CommandList

class TestCommands(unittest.TestCase):
    def test_get(self):
        command = CommandList.get('help')
        self.assertTrue(command and callable(command), 'Command get failed')
        
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