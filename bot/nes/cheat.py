import os
from interfaces.emuinput import EmuInput

class Cheat(EmuInput):
    destination = os.path.join(EmuInput.path, 'cheats.txt')

    def _validate_count(count):
        return count == 1

    def _validate_content(content):
        return content in ('run', 'attack')