import config
import unittest

from chat.twitchchat import TwitchChat


class TestChat(unittest.TestCase):
    def setUp(self):
        self.chat = TwitchChat(config.nick, config.password, config.host)

    def test_send(self):
        self.chat.send_message('Testing')

    def test_get(self):
        message = self.chat.get_message(timeout=2)
        self.assertTrue(message, 'Chat get failed')

    def tearDown(self):
        self.chat.close()