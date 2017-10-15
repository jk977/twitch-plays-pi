# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/permissions.py
# Compiled at: 2017-10-13 01:02:06
# Size of source mod 2**32: 590 bytes
import config
import unittest
from chat.message import Message
from chat.commands.admin import test_cmd
from tests.structs.dummychat import DummyChat

class TestPermissions(unittest.TestCase):

    def test_admin_command(self):
        fail_msg = 'Permissions test failed'
        chat = DummyChat()
        message = Message('steve', 'bar')
        result = test_cmd(chat, message)
        admin_message = Message(config.owner, 'foo')
        admin_result = test_cmd(chat, admin_message)
        self.assertTrue(admin_result, fail_msg)
        self.assertFalse(result, fail_msg)