# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/nes/buttons.py
# Compiled at: 2017-10-14 20:42:57
# Size of source mod 2**32: 1199 bytes
from interfaces.emuinputs import EmuInputs
from nes.button import Button

class Buttons(EmuInputs):
    limit = 9

    def __init__(self, *args):
        if not all((isinstance(b, Button) for b in args)):
            raise TypeError('Arguments must be Button objects.')
        buttons = Button.condense(args)
        inputs = []
        total = 0
        for b in buttons:
            if total + b.count > Buttons.limit:
                count = Buttons.limit - total
                inputs.append(Button(b.content, count))
                break
            else:
                total += b.count
                inputs.append(b)

        self._inputs = inputs

    @property
    def destination(self):
        return Button.destination

    @property
    def inputs(self):
        return self._inputs

    def serialize(self):
        return ' '.join((b.serialize() for b in self._inputs))

    def deserialize(serialized):
        buttons = []
        for i in serialized.split(' '):
            buttons.append(Button.deserialize(i))

        return Buttons(*)