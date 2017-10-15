# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/voting.py
# Compiled at: 2017-10-14 16:22:34
# Size of source mod 2**32: 1342 bytes
import unittest
from chat.user import User
from nes.choice import EmuChoice
from chat.voting.inputmanager import InputManager

def decision(choice):
    print(choice.name)


class TestVoting(unittest.TestCase):

    def setUp(self):
        self.vm1 = InputManager(threshold=1, on_decision=decision)
        self.vm2 = InputManager(threshold=2, on_decision=decision)
        self.u1 = User('bob')
        self.u2 = User('frank')
        self.c1 = EmuChoice('start*9')
        self.c2 = EmuChoice('A*3')
        print(self.c1._choice)
        print(self.c1._voters)

    def test_cast(self):
        fail_msg = 'Voting cast failed'
        self.assertTrue(self.vm1.cast_vote(self.u1, self.c1.name), fail_msg)
        self.assertTrue(self.vm1.cast_vote(self.u2, self.c1.name), fail_msg)
        self.assertFalse(self.vm2.cast_vote(self.u1, self.c1.name), fail_msg)
        self.assertFalse(self.vm2.cast_vote(self.u1, self.c2.name), fail_msg)
        self.assertTrue(self.vm2.cast_vote(self.u2, self.c2.name), fail_msg)
        self.assertFalse(self.vm2.cast_vote(self.u1, self.c1.name), fail_msg)
        self.assertTrue(self.vm2.remove_vote(self.u1, self.c1.name), fail_msg)
        self.assertFalse(self.vm2.cast_vote(self.u1, self.c1.name), fail_msg)
        self.assertTrue(self.vm2.cast_vote(self.u2, self.c1.name), fail_msg)