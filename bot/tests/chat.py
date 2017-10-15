import config
import unittest

from chat.twitchchat import TwitchChat


class TestChat(unittest.TestCase):
    def setUp(self):
        self.chat = TwitchChat(config.nick, config.password, config.owner)

    def test_send(self):
        self.chat.send_message('Testing')

    def test_get(self):
        try:
            message = self.chat.get_message(timeout=5)
            self.assertTrue(message, 'Chat get failed')
        except:
            self.assertTrue(False, 'Chat get failed (did you send anything?)')

    def tearDown(self):
        self.chat.close()