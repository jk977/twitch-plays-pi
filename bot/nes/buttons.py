from interfaces.emuinputs import EmuInputs
from nes.button import Button

class Buttons(EmuInputs):
    def __init__(self, *args):
        if not all(isinstance(b, Button) for b in args):
            raise TypeError('Arguments must be Button objects.')

        buttons = Button.condense(args)
        self._inputs = Buttons._truncate(buttons, 9)

    @property
    def destination(self):
        return Button.destination

    @property
    def inputs(self):
        return self._inputs

    def deserialize(serialized):
        buttons = []

        for i in serialized.split(' '):
            buttons.append(Button.deserialize(i))

        return Buttons(*buttons)