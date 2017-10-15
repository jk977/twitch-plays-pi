import config
import os
import unittest
from chat.twitchchat import TwitchChat

class TestChat(unittest.TestCase):

    def setUp(self):
        path = os.path.join(config.info_dir, 'oauth.cfg')
        self.chat = TwitchChat('shira_bot', config.password, '#shira_dummy')

    def test_send(self):
        self.chat.send_message('Testing')

    def tearDown(self):
        self.chat.close()