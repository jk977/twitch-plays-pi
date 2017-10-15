# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/commands.py
# Compiled at: 2017-10-14 02:02:54
# Size of source mod 2**32: 1053 bytes
import unittest
from chat.commands.commandlist import CommandList
from chat.commands.command import Command
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