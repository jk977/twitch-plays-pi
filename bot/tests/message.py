# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/message.py
# Compiled at: 2017-10-13 01:12:21
# Size of source mod 2**32: 774 bytes
import time
import unittest
from chat.message import Message

class TestMessage(unittest.TestCase):

    def test_constructor(self):
        fail_msg = 'Message constructor failed'
        author = 'bob'
        content = 'hi there'
        m_time = time.time()
        message = Message(author, content, m_time)
        self.assertEqual(message.author.name, author, fail_msg)
        self.assertEqual(message.content, content, fail_msg)
        self.assertEqual(message.timestamp, m_time, fail_msg)

    def test_serialize(self):
        message = Message('frank', 'howdy')
        ser = message.serialize()
        other = Message.deserialize(ser)
        self.assertEqual(message, other, 'Message serialization failed')


if __name__ == '__main__':
    unittest.main()