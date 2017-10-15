# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/tests/inputs.py
# Compiled at: 2017-10-14 20:34:06
# Size of source mod 2**32: 3897 bytes
import unittest
from nes.button import Button
from nes.buttons import Buttons
from nes.cheat import Cheat

class TestButtons(unittest.TestCase):

    def test_overflow(self):
        fail_msg = 'Buttons overflow failed'
        b1 = Button('start', 3)
        b2 = Button('select', 5)
        b3 = Button('A', 8)
        b4 = Button('A', 1)
        buttons = Buttons(b1, b2, b3)
        self.assertNotEqual(buttons.inputs, [b1, b2, b3], fail_msg)
        self.assertEqual(buttons.inputs, [b1, b2, b4], fail_msg)


class TestButton(unittest.TestCase):

    def test_condense(self):
        fail_msg = 'Button condense failed'
        buttons = [
         Button('start', 9), Button('start', 3), Button('up', 4), Button('start', 1)]
        condensed = Button.condense(buttons)
        self.assertNotEqual(buttons, condensed, fail_msg)
        self.assertEqual(condensed[0], Button('start', 12), fail_msg)

    def test_validation(self):
        fail_msg = 'Button validate failed'
        self.assertTrue(Button.validate('start*1'), fail_msg)
        self.assertTrue(Button.validate('select*2'), fail_msg)
        self.assertTrue(Button.validate('start*3'), fail_msg)
        self.assertTrue(Button.validate('up*4'), fail_msg)
        self.assertTrue(Button.validate('down*5'), fail_msg)
        self.assertTrue(Button.validate('left*6'), fail_msg)
        self.assertTrue(Button.validate('right*7'), fail_msg)
        self.assertTrue(Button.validate('A*8'), fail_msg)
        self.assertTrue(Button.validate('B*9'), fail_msg)
        self.assertFalse(Button.validate('1*start'), fail_msg)
        self.assertFalse(Button.validate('2*select'), fail_msg)
        self.assertFalse(Button.validate('3*start'), fail_msg)
        self.assertFalse(Button.validate('4*up'), fail_msg)
        self.assertFalse(Button.validate('5*down'), fail_msg)
        self.assertFalse(Button.validate('6*left'), fail_msg)
        self.assertFalse(Button.validate('7*right'), fail_msg)
        self.assertFalse(Button.validate('8*A'), fail_msg)
        self.assertFalse(Button.validate('9*B'), fail_msg)
        self.assertFalse(Button.validate('1start'), fail_msg)
        self.assertFalse(Button.validate('2select'), fail_msg)
        self.assertFalse(Button.validate('3start'), fail_msg)
        self.assertFalse(Button.validate('4up'), fail_msg)
        self.assertFalse(Button.validate('5down'), fail_msg)
        self.assertFalse(Button.validate('6left'), fail_msg)
        self.assertFalse(Button.validate('7right'), fail_msg)
        self.assertFalse(Button.validate('8A'), fail_msg)
        self.assertFalse(Button.validate('9B'), fail_msg)
        self.assertFalse(Button.validate('-1*A'), fail_msg)
        self.assertFalse(Button.validate('0*B'), fail_msg)
        self.assertFalse(Button.validate('10*select'), fail_msg)

    def test_constructor(self):
        fail_msg = 'Button constructor failed'
        button = Button('down', 4)
        self.assertEqual(button.count, 4, fail_msg)
        self.assertEqual(button.content, 'down', fail_msg)


class TestCheat(unittest.TestCase):

    def test_validate(self):
        fail_msg = 'Cheat validate failed'
        self.assertTrue(Cheat.validate('attack'), fail_msg)
        self.assertTrue(Cheat.validate('attack1'), fail_msg)
        self.assertTrue(Cheat.validate('run'), fail_msg)
        self.assertTrue(Cheat.validate('run*1'), fail_msg)
        self.assertFalse(Cheat.validate('2*run'), fail_msg)
        self.assertFalse(Cheat.validate('0*attack'), fail_msg)
        self.assertFalse(Cheat.validate('-1*run'), fail_msg)
        self.assertFalse(Cheat.validate('1attack'), fail_msg)

    def test_constructor(self):
        fail_msg = 'Cheat constructor failed'
        cheat = Cheat('run')
        self.assertEqual(cheat.count, 1, fail_msg)
        self.assertEqual(cheat.content, 'run', fail_msg)


if __name__ == '__main__':
    unittest.main()