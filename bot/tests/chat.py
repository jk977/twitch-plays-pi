import config
import unittest

from chat.twitchchat import TwitchChat

class TestChat(unittest.TestCase):
    def setUp(self):
        self.chat = TwitchChat('shira_bot', config.password, '#shira_dummy')

    def test_send(self):
        self.chat.send_message('Testing')

    def tearDown(self):
        self.chat.close()