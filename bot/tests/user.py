# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/user.py
# Compiled at: 2017-10-13 15:42:33
# Size of source mod 2**32: 1098 bytes
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

    def test_equals(self):
        fail_msg = 'User equals failed'
        u1 = User('stan')
        u2 = User('bill')
        u3 = User('stan')
        self.assertEqual(u1, u3, fail_msg)
        self.assertEqual(u2, u2, fail_msg)
        self.assertNotEqual(u1, u2, fail_msg)
        self.assertNotEqual(u3, u2, fail_msg)
        users = set([u1, u2, u3])
        self.assertEqual(len(users), 2, fail_msg)
        users.remove(u1)
        self.assertEqual(len(users), 1, fail_msg)