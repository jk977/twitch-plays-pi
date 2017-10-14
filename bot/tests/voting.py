import unittest

from chat.user import User
from chat.voting.choice import Choice
from chat.voting.inputmanager import InputManager

def decision(choice):
    print(choice.name)

class TestVoting(unittest.TestCase):
    def setUp(self):
        self.vm1 = InputManager(threshold=1, on_decision=decision)
        self.vm2 = InputManager(threshold=2, on_decision=decision)

        self.u1 = User('bob')
        self.u2 = User('frank')

        self.c1 = Choice('start*9')
        self.c2 = Choice('A*3')

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