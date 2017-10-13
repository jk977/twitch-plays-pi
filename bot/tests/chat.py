import config
import unittest
from chat.twitchchat import TwitchChat

class TestChat(unittest.TestCase):
    def setUp(self):
        with open(config.root + '/bot/info/oauth.cfg', 'r') as file:
            password = file.read().strip()

        self.chat = TwitchChat('shira_bot', password, '#shira_dummy')
        
    def test_send(self):
        self.chat.send_message('Testing')
        
    def test_get(self):
        fail_msg = 'Chat get failed'
        try:
            message = self.chat.get_message(3)
            self.assertTrue(message, fail_msg)
        except:
            self.assertTrue(False, fail_msg)
        
    def tearDown(self):
        self.chat.close()