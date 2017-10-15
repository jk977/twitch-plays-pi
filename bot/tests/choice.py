# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/choice.py
# Compiled at: 2017-10-14 20:21:51
# Size of source mod 2**32: 3926 bytes
import unittest
from chat.user import User
from nes.choice import EmuChoice
from chat.voting.choices import Choices

class TestChoices(unittest.TestCase):

    def setUp(self):
        self.u1 = User('fred')
        self.u2 = User('tony')
        c1 = EmuChoice('start*8', [self.u1])
        c2 = EmuChoice('up*1', [self.u2])
        c3 = EmuChoice('down*7 up*2')
        self.choices = Choices(c1, c2, c3)

    def test_add_choice(self):
        fail_msg = 'Choices add_choice failed'
        c1 = 'right*4'
        c2 = 'down*3'
        self.assertNotIn(c1, self.choices, fail_msg)
        self.assertNotIn(c2, self.choices, fail_msg)
        self.choices.add_choice(c1)
        self.choices.add_choice(c2)
        self.assertIn(c1, self.choices, fail_msg)
        self.assertIn(c2, self.choices, fail_msg)

    def test_add_vote(self):
        fail_msg = 'Choices add_vote failed'
        c1 = 'down*7 up*2'
        self.assertNotIn(self.u1, self.choices.get_voters(c1), fail_msg)
        self.assertTrue(self.choices.add_vote(self.u1, c1), fail_msg)
        self.assertIn(self.u1, self.choices.get_voters(c1), fail_msg)

    def test_remove_vote(self):
        fail_msg = 'Choices remove_vote failed'
        c1 = 'start*8'
        c2 = 'up*1'
        self.assertIn(self.u1, self.choices.get_voters(c1), fail_msg)
        self.assertIn(self.u2, self.choices.get_voters(c2), fail_msg)
        self.assertTrue(self.choices.remove_vote(self.u1, c1), fail_msg)
        self.assertTrue(self.choices.remove_vote(self.u2, c2), fail_msg)
        self.assertNotIn(self.u1, self.choices.get_voters(c1), fail_msg)
        self.assertNotIn(self.u2, self.choices.get_voters(c2), fail_msg)

    def test_equals(self):
        fail_msg = 'Choices equals failed'
        choices = Choices(EmuChoice('start*9'))
        self.assertEqual(self.choices, self.choices, fail_msg)
        self.assertNotEqual(self.choices, choices, fail_msg)

    def test_serialize(self):
        c1 = EmuChoice('start*9')
        c2 = EmuChoice('A*6')
        c3 = EmuChoice('down*1')
        choices = Choices(c1, c2, c3)
        ser = choices.serialize()
        deser = Choices.deserialize(ser)
        self.assertEqual(choices, deser, 'Choices serialize failed')


class TestEmuChoice(unittest.TestCase):

    def setUp(self):
        self.u1 = User('bob')
        self.u2 = User('steve')
        self.u3 = User('frank')

    def test_equals(self):
        fail_msg = 'EmuChoice constructor failed'
        n1 = 'down*7'
        v1 = [self.u1, self.u2]
        n2 = 'start*3'
        v2 = [self.u2, self.u3]
        c1 = EmuChoice(n1, v1)
        c2 = EmuChoice(n1, v2)
        c3 = EmuChoice(n2, v1)
        c4 = EmuChoice(n2, v2)
        c5 = EmuChoice(n1, v1)
        self.assertEqual(c1, c1, fail_msg)
        self.assertEqual(c2, c2, fail_msg)
        self.assertEqual(c3, c3, fail_msg)
        self.assertEqual(c4, c4, fail_msg)
        self.assertEqual(c1, c5, fail_msg)
        self.assertEqual(c1.name, n1, fail_msg)
        self.assertEqual(c2.name, n1, fail_msg)
        self.assertEqual(c3.name, n2, fail_msg)
        self.assertEqual(c4.name, n2, fail_msg)
        self.assertNotEqual(c1, c2, fail_msg)
        self.assertNotEqual(c2, c3, fail_msg)
        self.assertNotEqual(c3, c4, fail_msg)
        self.assertNotEqual(c1, c4, fail_msg)

    def test_vote(self):
        fail_msg = 'EmuChoice vote failed'
        choice = EmuChoice('run*1')
        self.assertFalse(choice.voters, fail_msg)
        choice.add_vote(self.u1)
        self.assertEqual(choice.votes, 1, fail_msg)
        self.assertIn(self.u1, choice.voters, fail_msg)

    def test_serialize(self):
        fail_msg = 'User serialize failed'
        user = User('bob')
        choice = EmuChoice('attack*1', [user])
        ser = choice.serialize()
        deser = EmuChoice.deserialize(ser)
        self.assertEqual(choice, deser, fail_msg)