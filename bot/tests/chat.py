import config
import os
import unittest
from chat.twitchchat import TwitchChat

class TestChat(unittest.TestCase):
    def setUp(self):
        path = os.path.join(config.info_dir, 'oauth.cfg')

        with open(path, 'r') as file:
            password = file.read().strip()

        self.chat = TwitchChat('shira_bot', password, '#shira_dummy')

    def test_send(self):
        self.chat.send_message('Testing')

    # uncomment if providing input through chat - will fail if no messages are sent manually
    #def test_get(self):
    #    fail_msg = 'Chat get failed'
    #    try:
    #        message = self.chat.get_message(5)
    #        success = all(bool(x) for x in [message.content, message.author])
    #        self.assertTrue(success, fail_msg)
    #    except:
    #        self.assertTrue(False, fail_msg)

    def tearDown(self):
        self.chat.close()