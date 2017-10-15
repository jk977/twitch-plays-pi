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