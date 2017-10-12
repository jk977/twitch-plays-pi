import unittest
from nes.button import Button
from nes.cheat import Cheat

class TestButton(unittest.TestCase): 
    def test_validation(self):
        fail_msg = 'Button validate failed'

        self.assertTrue(Button.validate('1*start'), fail_msg)
        self.assertTrue(Button.validate('2*select'), fail_msg)
        self.assertTrue(Button.validate('3*start'), fail_msg)
        self.assertTrue(Button.validate('4*up'), fail_msg)
        self.assertTrue(Button.validate('5*down'), fail_msg)
        self.assertTrue(Button.validate('6*left'), fail_msg)
        self.assertTrue(Button.validate('7*right'), fail_msg)
        self.assertTrue(Button.validate('8*A'), fail_msg)
        self.assertTrue(Button.validate('9*B'), fail_msg)

        self.assertFalse(Button.validate('start*1'), fail_msg)
        self.assertFalse(Button.validate('select*2'), fail_msg)
        self.assertFalse(Button.validate('start*3'), fail_msg)
        self.assertFalse(Button.validate('up*4'), fail_msg)
        self.assertFalse(Button.validate('down*5'), fail_msg)
        self.assertFalse(Button.validate('left*6'), fail_msg)
        self.assertFalse(Button.validate('right*7'), fail_msg)
        self.assertFalse(Button.validate('A*8'), fail_msg)
        self.assertFalse(Button.validate('B*9'), fail_msg)

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

        self.assertTrue(Cheat.validate('1*run'), fail_msg)
        self.assertTrue(Cheat.validate('1*attack'), fail_msg)

        self.assertFalse(Cheat.validate('-1*run'), fail_msg)
        self.assertFalse(Cheat.validate('2*attack'), fail_msg)
        self.assertFalse(Cheat.validate('attack*1'), fail_msg)

    def test_constructor(self):
        fail_msg = 'Cheat constructor failed'

        cheat = Cheat('run')
        self.assertEqual(cheat.count, 1, fail_msg)
        self.assertEqual(cheat.content, 'run', fail_msg)