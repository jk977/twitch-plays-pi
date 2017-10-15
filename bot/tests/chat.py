# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/chat.py
# Compiled at: 2017-10-14 01:13:18
# Size of source mod 2**32: 798 bytes
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