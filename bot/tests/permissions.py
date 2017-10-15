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