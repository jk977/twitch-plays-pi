from chat.user import User
from interfaces.choice import Choice
from interfaces.emuinput import EmuInput
from nes.buttons import Buttons
from nes.cheat import Cheat

class EmuChoice(Choice):
    def __init__(self, choice, voters=set()):
        """
        Initializes EmuChoice object, containing EmuInput object and list of Users.
        :param choice: EmuInput object or name of choice.
        :param voters: List of Users that voted for choice.
        """
        voters = set(voters)

        if not all((isinstance(voter, User) for voter in voters)):
            raise ValueError('Voters must be an iterable containing Users.')

        if isinstance(choice, EmuInput):
            pass
        elif Cheat.validate(choice):
            choice = Cheat.deserialize(choice)
        else:
            if Buttons.validate(choice):
                choice = Buttons.deserialize(choice)
            else:
                raise ValueError('Choice "{}" is not a valid emulator input.'.format(choice))

        self._choice = choice
        self._voters = voters

    @property
    def destination(self):
        return self._choice.destination

    @property
    def input(self):
        return self._choice

    @property
    def name(self):
        return self._choice.serialize()