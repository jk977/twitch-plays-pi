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

        return Buttons(*buttons)