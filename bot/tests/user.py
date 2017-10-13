import config
import unittest
from chat.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User('bob')

    def test_properties(self):
        fail_msg = 'User properties failed'

        owner = User(config.owner)

        self.assertEqual(self.user.name, 'bob', 'User constructor failed')
        self.assertFalse(self.user.admin, fail_msg)
        self.assertTrue(owner.admin, fail_msg)

    def test_serialize(self):
        ser = self.user.serialize()
        user = User.deserialize(ser)
        self.assertEqual(self.user, user, 'User serialize failed')